from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    llm_model: str = "gpt-4.1-mini"
    chunk_size: int = 500
    chunk_overlap: int = 50
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str = "ai-rag-platform"
    PINECONE_EMBEDDING_MODEL: str = "llama-text-embed-v2"
    GROQ_API_KEY: str | None = None
    aws_region: str
    cognito_user_pool_id: str
    cognito_client_id: str
    cognito_client_secret: str
    session_secret_key: str
    session_cookie_secure: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()