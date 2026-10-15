from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"
    mongo_database: str = "cardapio_web"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
settings = Settings()