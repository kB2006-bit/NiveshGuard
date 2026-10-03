from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NiveshGuard API"
    DATABASE_URL: str = "sqlite:///./test.db"
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "llama3"
    SECRET_KEY: str = "dev_secret_key_replace_in_prod"
    
    class Config:
        env_file = ".env"

settings = Settings()
