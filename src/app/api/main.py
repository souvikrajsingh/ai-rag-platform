from urllib.parse import urlsplit, urlunsplit

from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from src.app.api.auth import get_session_user
from src.app.api.route import router
from src.app.config.settings import settings

app = FastAPI(title="RAG")
app.include_router(router)
frontend_url = settings.frontend_url.rstrip("/")
frontend_origins = [
    origin.strip().rstrip("/")
    for origin in settings.frontend_origins.split(",")
    if origin.strip()
]
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
    https_only=settings.session_cookie_secure,
    same_site=settings.session_cookie_same_site,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth = OAuth()
oauth.register(
    name="oidc",
    client_id=settings.cognito_client_id,
    client_secret=settings.cognito_client_secret,
    server_metadata_url=(
        f"https://cognito-idp.{settings.aws_region}.amazonaws.com/"
        f"{settings.cognito_user_pool_id}/.well-known/openid-configuration"
    ),
    client_kwargs={"scope": "phone openid email"},
)

@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url=frontend_url, status_code=307)


@app.get("/login", name="login", include_in_schema=False)
async def login(request: Request):
    if get_session_user(request) is not None:
        return RedirectResponse(url=frontend_url, status_code=303)
    redirect_uri = request.url_for("auth_callback")
    return await oauth.oidc.authorize_redirect(request, redirect_uri)


@app.get("/signup", name="signup", include_in_schema=False)
async def signup(request: Request):
    if get_session_user(request) is not None:
        return RedirectResponse(url=frontend_url, status_code=303)
    redirect_uri = request.url_for("auth_callback")
    response = await oauth.oidc.authorize_redirect(request, redirect_uri)
    location = response.headers.get("location")
    if location is None:
        raise HTTPException(
            status_code=502,
            detail="Cognito did not provide an authorization URL for sign-up.",
        )
    signup_url = urlsplit(location)._replace(path="/signup").geturl()
    return RedirectResponse(url=signup_url, status_code=response.status_code)


@app.get("/auth/callback", name="auth_callback", include_in_schema=False)
async def auth_callback(request: Request):
    token = await oauth.oidc.authorize_access_token(request)
    userinfo = token.get("userinfo")
    if userinfo is None or not userinfo.get("sub"):
        raise HTTPException(
            status_code=502,
            detail="Cognito did not return a user identity for the OIDC login.",
        )
    request.session["user"] = dict(userinfo)
    return RedirectResponse(url=frontend_url, status_code=303)


@app.get("/logout", name="logout", include_in_schema=False)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=f"{frontend_url}/login.html", status_code=303)