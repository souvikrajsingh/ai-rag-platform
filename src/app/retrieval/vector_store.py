import hashlib
from pathlib import Path

from langchain_core.documents import Document
from pinecone import Pinecone

from src.app.config.settings import settings


class VectorStore:
    def __init__(self):
        client = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = client.Index(settings.PINECONE_INDEX_NAME)

    def namespaces(self) -> set[str]:
        stats = self.index.describe_index_stats()
        return {
            namespace
            for namespace, details in stats.namespaces.items()
            if details.vector_count > 0
        }

    def upsert(self, documents: list[Document]) -> int:
        batch_size = 96
        namespaces: dict[str, list[Document]] = {}
        for document in documents:
            source = str(document.metadata.get("source", "unknown"))
            namespace = Path(source).name
            namespaces.setdefault(namespace, []).append(document)

        for namespace, namespace_documents in namespaces.items():
            for start in range(0, len(namespace_documents), batch_size):
                batch = namespace_documents[start : start + batch_size]
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

    def search(self, query: str, k: int = 3) -> list[Document]:
        namespaces = self.index.describe_index_stats().namespaces
        matches = []
        for namespace in namespaces:
            response = self.index.search(
                namespace=namespace,
                top_k=k,
                inputs={"text": query},
                fields=["text", "source", "page", "page_number"],
            )
            matches.extend(response.result.hits)

        documents = []
        for match in sorted(matches, key=lambda match: match.score, reverse=True)[:k]:
            fields = dict(match.fields or {})
            try:
                page_content = fields.pop("text")
            except KeyError as error:
                raise ValueError(
                    f"Pinecone result {match.id!r} is missing its text field."
                ) from error
            documents.append(Document(page_content=page_content, metadata=fields))

        return documents
