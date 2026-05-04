from src.medinfo_agent.prompts import CONTENT_GENERATION_SYSTEM_PROMPT
from src.llm_models import llm_model
from src.tools import retrieve_articles_from_qdrant, think_tool


medical_content_agent = {
    "name": "medical_content_agent",
    "description": "Generate introduction and discussion text for medical writing from the provided PMIDs.",
    "system_prompt": CONTENT_GENERATION_SYSTEM_PROMPT,
    "tools": [retrieve_articles_from_qdrant, think_tool],
    "model": llm_model,
}
