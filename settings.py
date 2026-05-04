from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",
    )
  azure_deployment:str = Field(alias='AZURE_OPENAI_DEPLOYMENT')
  azure_endpoint:str=Field(alias='AZURE_OPENAI_ENDPOINT')
  azure_api_key:str = Field(alias='AZURE_OPENAI_API_KEY')
  azure_embedding_deployment:str=Field(alias='AZURE_OPENAI_EMBEDDING_DEPLOYMENT')
  tavily_api_key:str=Field(alias='TAVILY_API_KEY')
  langsmith_api_key:str=Field(alias='LANGSMITH_API_KEY')
  langsmith_tracing:bool=Field(alias='LANGSMITH_TRACING')
  db_url:str=Field(alias='DB_URI')
  clerk_secret_key:str=Field(alias='CLERK_SECRET_KEY')
  qudrant_url:str=Field(alias='QUDRANT_URL')
  qudrant_api_key:str=Field(alias='QUDRANT_API_KEY')

app_settings = Settings()
