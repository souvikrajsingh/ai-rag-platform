from langchain_community.document_loaders import PyPDFLoader

class DocumentLoader:
    def load(self, file_path: str):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents   