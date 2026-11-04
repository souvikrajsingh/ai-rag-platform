from pathlib import Path
from typing import BinaryIO

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pypdf import PdfReader

class DocumentLoader:
    def load(self, file_path: str):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents

    def load_stream(self, file: BinaryIO, filename: str) -> list[Document]:
        reader = PdfReader(file)
        metadata = {
            key.lstrip("/").lower(): str(value)
            for key, value in (reader.metadata or {}).items()
            if value is not None
        }
        source = Path(filename).name

        return [
            Document(
                page_content=page.extract_text() or "",
                metadata={
                    **metadata,
                    "source": source,
                    "page": page_number,
                    "total_pages": len(reader.pages),
                },
            )
            for page_number, page in enumerate(reader.pages)
        ]