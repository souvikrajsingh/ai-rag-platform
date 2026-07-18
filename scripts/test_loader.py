from src.app.ingestion.document_loader import DocumentLoader

loader = DocumentLoader()

documents = loader.load("data/raw/python_lec01.pdf")

print(type(documents))
print(len(documents))
print(documents[0].page_content[:300])
print(documents[0].metadata)