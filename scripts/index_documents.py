from pathlib import Path
import time

from src.app.ingestion.document_loader import DocumentLoader
from src.app.ingestion.text_splitter import TextSplitter
from src.app.embedding.embedding_manager import EmbeddingManager
from src.app.retrieval.vector_store import VectorStore
from src.app.util.hash_manager import HashManager

# Create objects
loader = DocumentLoader()
splitter = TextSplitter()
embedding_manager = EmbeddingManager()
hash_manager = HashManager()

vector_store = VectorStore(
    embedding_manager.embedding_model
)

folder_path = Path("data/raw")
vector_store_path = Path("data/vector_store")

# Load existing vector store if it exists
if (vector_store_path / "index.faiss").exists():
    print("Loading existing vector store...")
    vector_store.load(str(vector_store_path))
    index_exists = True
else:
    print("Creating new vector store...")
    index_exists = False

# Load previously indexed hashes
hashes = hash_manager.load_hashes()

start = time.time()

# Process every PDF
for pdf_file in folder_path.glob("*.pdf"):

    current_hash = hash_manager.calculate_hash(pdf_file)
    old_hash = hashes.get(pdf_file.name)

    # Skip unchanged files
    if old_hash == current_hash:
        print(f"Skipping: {pdf_file.name}")
        continue

    print(f"Indexing: {pdf_file.name}")

    # Load and split only this PDF
    documents = loader.load(str(pdf_file))
    chunks = splitter.split(documents)

    print(f"Pages: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    # First PDF ever -> Create index
    if not index_exists:
        vector_store.create(chunks)
        index_exists = True
    else:
        vector_store.add(chunks)

    # Update stored hash
    hashes[pdf_file.name] = current_hash

# Save only if a vector store exists
if index_exists:
    vector_store.save("data/vector_store")

# Save updated hashes
hash_manager.save_hashes(hashes)

end = time.time()

print("\nIndexing complete!")
print(f"Total Time: {end - start:.2f} seconds")