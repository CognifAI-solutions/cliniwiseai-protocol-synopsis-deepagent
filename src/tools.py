from datetime import datetime
import json
import time
import logging
from typing import List, Literal
from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langchain.tools import ToolRuntime
from langgraph.types import Command
from deepagents.backends.utils import create_file_data
from requests.exceptions import ConnectionError, Timeout
from openai import AzureOpenAI

from settings import app_settings

logger = logging.getLogger(__name__)

tavily_client = TavilyClient(api_key=app_settings.tavily_api_key)

MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # seconds


image_model = AzureOpenAI(
    api_version="2025-04-01-preview",
    api_key=app_settings.azure_api_key,
    azure_endpoint=app_settings.azure_endpoint,
)


def _retry_tavily_call(func, *args, **kwargs):
    """Retry a Tavily API call with exponential backoff on transient network errors."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return func(*args, **kwargs)
        except (ConnectionError, Timeout, OSError) as exc:
            if attempt == MAX_RETRIES:
                raise
            wait = RETRY_BACKOFF_BASE**attempt
            logger.warning(
                "Tavily API call failed (attempt %d/%d): %s. Retrying in %ds...",
                attempt,
                MAX_RETRIES,
                exc,
                wait,
            )
            time.sleep(wait)


@tool(parse_docstring=True)
def internet_search(query: str, max_results: int = 15) -> str:
    """Run a web search.

    Args:
        query: The search query text.
        max_results: The maximum number of search results to return.

    Returns:
        A JSON string containing search results.
    """
    result = _retry_tavily_call(
        tavily_client.search, query=query, max_results=max_results
    )
    try:
        return json.dumps(result)
    except Exception as e:
        logger.error(f"Error searching internet: {e}")
        return f"Error searching internet: {e}"


@tool(parse_docstring=True)
def extract_webpage(
    urls: List[str],
    file_path: str,
    extract_depth: Literal["basic", "advanced"] = "basic",
    runtime: ToolRuntime = None,
) -> Command | str:
    """Extract webpage content from the provided URLs.

    Args:
        urls: A list of URLs to extract content from.
        file_path: Absolute path (starting with /) to save the extracted content to the filesystem.

    Returns:
        Dict with extraction operation result.
        if successful: {"status":"success","message":"File extracted and saved to the file system"}
        if failure: {"status":"error","message":f"Error extracting webpage: {e}"}
    """
    try:
        response = _retry_tavily_call(
            tavily_client.extract, urls, format="markdown", extract_depth=extract_depth
        )
        if file_path and runtime:

            content = ""
            for result in response["results"]:
                content += (
                    "Source: " + result["url"] + "\n\n" + result["raw_content"] + "\n"
                )
                content += "----------------------------------------\n"
            content = content.strip()
            file_data = create_file_data(content)
            return Command(
                update={
                    "files": {file_path: file_data},
                    "messages": [
                        ToolMessage(
                            content=f"Extracted webpage content saved to {file_path} ({len(content)} characters)",
                            tool_call_id=runtime.tool_call_id,
                        )
                    ],
                }
            )
        return {
            "status": "success",
            "message": "File extracted and saved to the file system",
        }
    except Exception as e:
        logger.error(f"Error extracting webpage: {e}")
        return {"status": "error", "message": f"Error extracting webpage: {e}"}


@tool(parse_docstring=True)
def generate_image(
    prompt: str,
    file_path: str,
    runtime: ToolRuntime = None,
):
    """Generate Image and save it to filesystem

    Args:
        prompt: A very descriptive prompt about the image to be generated for the image generation model
        file_path: Absolute path (starting with /) to save the extracted content to the filesystem.

    Returns:
        Dict with image operation result.
        if successful: {"status":"success","message":"Image generated and saved to the file system"}
        if failure: {"status":"error","message":f"Error generating image: {e}"}
    """
    try:
        response = image_model.images.generate(
            model="gpt-image-1.5",
            prompt=prompt,
            n=1,
            quality="high",
            output_format="png",
        )
        image_base64 = response.data[0].b64_json
        file_data = create_file_data(content=image_base64, encoding="base64")
        return Command(
                update={
                    "files": {file_path: file_data},
                    "messages": [
                        ToolMessage(
                            content=f"Image saved to {file_path})",
                            tool_call_id=runtime.tool_call_id,
                        )
                    ],
                }
            )
    except Exception as e:
        logger.error(f"Error generating image:{e}")
        return {"status": "error", "message": f"Error generating image:{e}"}


@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: A detailed reflection on research progress, findings, gaps,
            and next steps.

    Returns:
        A confirmation message indicating that reflection was recorded.
    """
    return f"Reflection recorded: {reflection}"


@tool(parse_docstring=True)
def write_output(markdown_content: str) -> str:
    """Write final output to a markdown file.

    Args:
        markdown_content: Final content in markdown format.

    Returns:
        Dict with write operation result.
        if successful: {"status":"success","message":"Output saved successfully"}
        if failure: {"status":"failed","message":"Error saving the output"}
    """
    current_date_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    file_path = f"output_file_{current_date_time}.md"
    try:
        with open(file_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
    except OSError as exc:
        print(f"Error writing markdown file: {exc}")
