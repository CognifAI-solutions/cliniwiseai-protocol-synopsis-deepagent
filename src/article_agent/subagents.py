from src.llm_models import llm_model_mini
from src.article_agent.prompts import RESEARCH_SUBAGENT_PROMPT
from src.tools import extract_webpage, internet_search, think_tool, extract_webpage_and_save


research_agent = {
    "name": "research_agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "system_prompt": RESEARCH_SUBAGENT_PROMPT,
    "tools": [internet_search, extract_webpage_and_save, extract_webpage, think_tool],
    "model": llm_model_mini,
}
