from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Expensas Claras"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:5173"]

    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_api_key: str = ""

    user_state_store: str = "memory"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
