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

# Load the PDF
documents = loader.load("data/raw/python_lec10.pdf")

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
# vectors = embedding_manager.embed(chunks)

# print(f"Embeddings Generated: {len(vectors)}")

# print(f"Dimension of first embedding: {len(vectors[0])}")

# print("\nFirst 10 values of the first embedding:")
# print(vectors[0][:10])


# Create FAISS Index
faiss_index = vector_store.create(chunks)

print("Vector Store Created Successfully!")

print(f"Number of chunks indexed: {faiss_index.index.ntotal}")

print(f"Embedding Dimension: {faiss_index.index.d}")

query = "What is a Python dictionary?"

results = vector_store.search(query)

print("\n=== Search Results ===")
print(f"Results Found: {len(results)}")

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(doc.page_content[:300])
