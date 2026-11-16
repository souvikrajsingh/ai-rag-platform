import os
import sys
import types
import unittest
from unittest.mock import AsyncMock, Mock, patch
from urllib.parse import parse_qs, urlsplit

for key, value in {
    "GEMINI_API_KEY": "test-gemini-key",
    "PINECONE_API_KEY": "test-pinecone-key",
    "AWS_REGION": "ap-southeast-2",
    "COGNITO_USER_POOL_ID": "test-user-pool",
    "COGNITO_CLIENT_ID": "test-client",
    "COGNITO_CLIENT_SECRET": "test-client-secret",
    "SESSION_SECRET_KEY": "test-session-secret",
}.items():
    os.environ.setdefault(key, value)

from fastapi.responses import RedirectResponse
from fastapi.testclient import TestClient

dependencies = types.ModuleType("src.app.api.dependencies")
dependencies.vector_store = Mock()
dependencies.rag_service = Mock()
dependencies.ingestion_service = Mock()
sys.modules["src.app.api.dependencies"] = dependencies

from src.app.api.main import app, frontend_origins, frontend_url, oauth


class CognitoSignupTests(unittest.TestCase):
    def test_backend_landing_redirects_to_frontend(self):
        response = TestClient(app).get("/", follow_redirects=False)
        self.assertEqual(response.status_code, 307)
        self.assertEqual(response.headers["location"], frontend_url)

    def test_frontend_origin_can_make_credentialed_cors_requests(self):
        frontend_origin = frontend_origins[0]
        response = TestClient(app).options(
            "/documents",
            headers={
                "Origin": frontend_origin,
                "Access-Control-Request-Method": "GET",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["access-control-allow-origin"],
            frontend_origin,
        )
        self.assertEqual(response.headers["access-control-allow-credentials"], "true")

    def test_logout_returns_user_to_frontend_sign_in_page(self):
        response = TestClient(app).get("/logout", follow_redirects=False)
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["location"], frontend_url)

    def test_auth_callback_redirects_to_chat(self):
        with patch.object(
            oauth.oidc,
            "authorize_access_token",
            new=AsyncMock(return_value={"userinfo": {"sub": "test-user"}}),
        ):
            response = TestClient(app).get(
                "/auth/callback",
                follow_redirects=False,
            )

        self.assertEqual(response.status_code, 303)
        self.assertEqual(
            response.headers["location"],
            f"{frontend_url}/chat",
        )

    def test_signup_preserves_authlib_state_and_redirect_parameters(self):
        authorize_response = RedirectResponse(
            "https://cognito.example/oauth2/authorize"
            "?client_id=test&state=auth-state"
            "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauth%2Fcallback",
            status_code=302,
        )
        with patch.object(
            oauth.oidc,
            "authorize_redirect",
            new=AsyncMock(return_value=authorize_response),
        ):
            response = TestClient(app).get("/signup", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        location = urlsplit(response.headers["location"])
        self.assertEqual(location.path, "/signup")
        query = parse_qs(location.query)
        self.assertEqual(query["state"], ["auth-state"])
        self.assertEqual(query["client_id"], ["test"])


if __name__ == "__main__":
    unittest.main()
