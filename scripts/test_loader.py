from src.app.ingestion.document_loader import DocumentLoader
from src.app.ingestion.text_splitter import TextSplitter
from src.app.embedding.embedding_manager import EmbeddingManager

# Create objects
loader = DocumentLoader()
splitter = TextSplitter()
embedding_manager = EmbeddingManager()

# Load the PDF
documents = loader.load("data/raw/python_lec01.pdf")

print("=== Document Loader ===")
print(f"Type: {type(documents)}")
print(f"Pages Loaded: {len(documents)}")
print(documents[0].page_content[:300])
print(documents[0].metadata)

# Split into chunks
chunks = splitter.split(documents)

print("\n=== Text Splitter ===")
print(f"Chunks Created: {len(chunks)}")
print(chunks[0].page_content[:300])
print(chunks[0].metadata)

# Generate embeddings
vectors = embedding_manager.embed(chunks)

print(f"Embeddings Generated: {len(vectors)}")

print(f"Dimension of first embedding: {len(vectors[0])}")

print("\nFirst 10 values of the first embedding:")
print(vectors[0][:10])