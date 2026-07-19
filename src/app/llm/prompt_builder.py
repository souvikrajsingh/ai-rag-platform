from langchain_core.documents import Document


class PromptBuilder:

    def build(
        self,
        question: str,
        documents: list[Document]
    ) -> str:

        context = "\n\n".join(
            doc.page_content
            for doc in documents
        )

        prompt = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the context below.

If the answer is not present in the context, say:
"I don't have enough information to answer that."
Don't make up facts, refer thoroughly to the context, if its even related
to the question asked

Context:
{context}

Question:
{question}

Answer:
"""

        return prompt