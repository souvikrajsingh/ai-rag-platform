from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    llm_model: str = "gpt-4.1-mini"
    chunk_size: int = 500
    chunk_overlap: int = 50
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str = "ai-rag-platform"
    PINECONE_EMBEDDING_MODEL: str = "llama-text-embed-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()