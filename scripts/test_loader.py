from src.app.ingestion.document_loader import DocumentLoader
from src.app.ingestion.text_splitter import TextSplitter
from src.app.embedding.embedding_manager import EmbeddingManager
from src.app.retrieval.vector_store import VectorStore
from src.app.llm.prompt_builder import PromptBuilder
from src.app.llm.llm_manager import LLMManager
from src.app.services.rag_service import RAGService

# Create objects
loader = DocumentLoader()
splitter = TextSplitter()
embedding_manager = EmbeddingManager()
vector_store = VectorStore(
    embedding_manager.embedding_model
)
# prompt_builder = PromptBuilder()
# llm_manager = LLMManager()
rag_service = RAGService(vector_store)

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

vector_store.save("data/vector_store")

print("Index Saved")

new_vector_store = VectorStore(
    embedding_manager.embedding_model
)

new_vector_store.load("data/vector_store")
print("Index Loaded")



# print("Vector Store Created Successfully!")

# print(f"Number of chunks indexed: {faiss_index.index.ntotal}")

# print(f"Embedding Dimension: {faiss_index.index.d}")

query = "What is a Python dictionary?"

results = new_vector_store.search(query)

print("\n=== Search Results ===")
print(f"Results Found: {len(results)}")

# for i, doc in enumerate(results, start=1):
#     print(f"\nResult {i}")
#     print("-" * 40)
#     print(doc.page_content[:300])

# print("\n=== Testing prompt Builder ===")

# prompt = prompt_builder.build(query, results)

# print("\n=== PROMPT BELOW ===")
# print(prompt)

# answer = llm_manager.generate(prompt)

# print("\n=== Final Answer ===")
# print(answer)


# implement rag service

answer = rag_service.ask(query)
print (answer)


