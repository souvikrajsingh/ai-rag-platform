from pathlib import Path
import time

from src.app.ingestion.document_loader import DocumentLoader
from src.app.ingestion.text_splitter import TextSplitter
from src.app.embedding.embedding_manager import EmbeddingManager
from src.app.retrieval.vector_store import VectorStore

# Create objects
loader = DocumentLoader()
splitter = TextSplitter()
embedding_manager = EmbeddingManager()

vector_store = VectorStore(
    embedding_manager.embedding_model
)

folder_path = Path("data/raw")

all_documents = []

start = time.time()

# Load every PDF inside data/raw
for pdf_file in folder_path.glob("*.pdf"):
    print(f"Loading: {pdf_file.name}")

    documents = loader.load(str(pdf_file))
    all_documents.extend(documents)

print(f"\nTotal Pages Loaded: {len(all_documents)}")

# Split all documents
chunks = splitter.split(all_documents)

print(f"Total Chunks Created: {len(chunks)}")

# Create FAISS index
vector_store.create(chunks)

# Save index
vector_store.save("data/vector_store")

end = time.time()

print("\nVector store created successfully!")
print(f"Total Time: {end - start:.2f} seconds")