import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

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

from fastapi import HTTPException
from langchain_core.documents import Document
from starlette.requests import Request

from src.app.api.auth import (
    namespace_for_user,
    require_authenticated_user,
)
from src.app.retrieval.vector_store import VectorStore
from src.app.util.hash_manager import HashManager


class UserNamespaceTests(unittest.TestCase):
    def test_namespace_is_stable_and_distinct_per_user(self):
        first = namespace_for_user("cognito-sub-a")
        self.assertEqual(first, namespace_for_user("cognito-sub-a"))
        self.assertNotEqual(first, namespace_for_user("cognito-sub-b"))

    def test_api_user_requires_a_cognito_sub(self):
        request = Request({"type": "http", "headers": [], "session": {}})
        with self.assertRaises(HTTPException) as error:
            require_authenticated_user(request)
        self.assertEqual(error.exception.status_code, 401)

        request = Request(
            {
                "type": "http",
                "headers": [],
                "session": {"user": {"sub": "cognito-sub-a"}},
            }
        )
        self.assertEqual(
            require_authenticated_user(request)["sub"],
            "cognito-sub-a",
        )

    def test_user_upload_manifests_are_separate(self):
        first_namespace = namespace_for_user("cognito-sub-a")
        second_namespace = namespace_for_user("cognito-sub-b")
        with tempfile.TemporaryDirectory() as temporary_directory:
            original_directory = Path.cwd()
            os.chdir(temporary_directory)
            try:
                HashManager(first_namespace).save_hashes(
                    {"first.pdf": "first-hash"}
                )
                self.assertEqual(
                    HashManager(first_namespace).load_hashes(),
                    {"first.pdf": "first-hash"},
                )
                self.assertEqual(
                    HashManager(second_namespace).load_hashes(),
                    {},
                )
            finally:
                os.chdir(original_directory)

    def test_vector_store_upserts_and_searches_only_given_namespace(self):
        store = VectorStore.__new__(VectorStore)
        store.index = Mock()
        store.index.search.return_value = SimpleNamespace(
            result=SimpleNamespace(hits=[])
        )
        first_namespace = namespace_for_user("cognito-sub-a")
        second_namespace = namespace_for_user("cognito-sub-b")

        store.upsert(
            [Document(page_content="private text", metadata={"source": "a.pdf"})],
            first_namespace,
        )
        store.search("question", first_namespace)
        store.search("question", second_namespace)

        self.assertEqual(
            store.index.upsert_records.call_args.kwargs["namespace"],
            first_namespace,
        )
        self.assertEqual(
            [
                call.kwargs["namespace"]
                for call in store.index.search.call_args_list
            ],
            [first_namespace, second_namespace],
        )


if __name__ == "__main__":
    unittest.main()
