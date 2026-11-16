import hashlib

from langchain_core.documents import Document
from pinecone import Pinecone

from src.app.config.settings import settings


class VectorStore:
    def __init__(self):
        client = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = client.Index(settings.PINECONE_INDEX_NAME)

    def has_namespace(self, namespace: str) -> bool:
        stats = self.index.describe_index_stats()
        namespaces = stats.namespaces or {}
        return (
            namespace in namespaces
            and namespaces[namespace].vector_count > 0
        )

    def upsert(self, documents: list[Document], namespace: str) -> int:
        batch_size = 96
        for start in range(0, len(documents), batch_size):
            batch = documents[start : start + batch_size]
            records = [
                {
                    "_id": hashlib.sha256(
                        "\0".join(
                            (
                                str(document.metadata.get("source", "")),
                                str(
                                    document.metadata.get(
                                        "page",
                                        document.metadata.get("page_number", ""),
                                    )
                                ),
                                document.page_content,
                            )
                        ).encode("utf-8")
                    ).hexdigest(),
                    "text": document.page_content,
                    **{
                        key: value
                        for key, value in document.metadata.items()
                        if key not in {"_id", "id", "text"}
                        and isinstance(value, (str, int, float, bool))
                    },
                }
                for document in batch
            ]
            self.index.upsert_records(records=records, namespace=namespace)

        return len(documents)

    def search(
        self, query: str, namespace: str, k: int = 3
    ) -> list[Document]:
        response = self.index.search(
            namespace=namespace,
            top_k=k,
            inputs={"text": query},
            fields=["text", "source", "page", "page_number"],
        )
        matches = response.result.hits

        documents = []
        for match in sorted(
            matches, key=lambda match: match.score, reverse=True
        )[:k]:
            fields = dict(match.fields or {})
            try:
                page_content = fields.pop("text")
            except KeyError as error:
                raise ValueError(
                    f"Pinecone result {match.id!r} is missing its text field."
                ) from error
            documents.append(Document(page_content=page_content, metadata=fields))

        return documents
