from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    DB_CONNECTION: str
    PASSWORD_SECRET: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME: int

settings = Settings()