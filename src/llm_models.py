from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from settings import app_settings

image_model = AzureOpenAI(
    api_version="2025-04-01-preview",
    api_key=app_settings.azure_api_key,
    azure_endpoint=app_settings.azure_endpoint,
    azure_deployment="gpt-image-1.5",
)


llm_model = AzureChatOpenAI(
    model="gpt-5.4",
    azure_deployment=app_settings.azure_deployment,
    api_version="2025-04-01-preview",
    api_key=app_settings.azure_api_key,
    azure_endpoint=app_settings.azure_endpoint,
    use_responses_api=True,
    service_tier="priority",
)

llm_model_mini = AzureChatOpenAI(
    model="gpt-5.4-mini",
    azure_deployment=app_settings.azure_deployment,
    api_version="2025-04-01-preview",
    api_key=app_settings.azure_api_key,
    azure_endpoint=app_settings.azure_endpoint,
    use_responses_api=True,
)

embedding_model = AzureOpenAIEmbeddings(
    azure_endpoint=app_settings.azure_endpoint,
    model="text-embedding-3-large",
    api_key=app_settings.azure_api_key,
    azure_deployment=app_settings.azure_embedding_deployment,
    api_version="2024-02-01",
)
