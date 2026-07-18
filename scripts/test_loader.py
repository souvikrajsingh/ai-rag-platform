from src.app.ingestion.document_loader import DocumentLoader
from src.app.ingestion.text_splitter import TextSplitter

# Create objects
loader = DocumentLoader()
splitter = TextSplitter()

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