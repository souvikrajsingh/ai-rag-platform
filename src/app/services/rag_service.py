from src.app.retrieval.vector_store import VectorStore
from src.app.llm.prompt_builder import PromptBuilder
from src.app.llm.llm_manager import LLMManager


class RAGService:

    def __init__(
        self,
        vector_store: VectorStore,
    ):
        self.vector_store = vector_store
        self.prompt_builder = PromptBuilder()
        self.llm_manager = LLMManager()

    def ask(self, question: str):
        documents = self.vector_store.search(question)

        prompt = self.prompt_builder.build(question,documents)

        answer = self.llm_manager.generate(prompt)

        return answer