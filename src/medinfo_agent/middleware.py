"""PMID tracking middleware for the medinfo agent.

Adds a custom `pmids` field to the agent state and exposes a `write_pmids`
tool that replaces the entire PMID list, mirroring the `write_todos` pattern
documented at:
https://docs.langchain.com/oss/python/deepagents/frontend/todo-list#custom-state-beyond-todos

The middleware does NOT inject anything into the system prompt. The agent
discovers `write_pmids` purely through its tool description, and the `pmids`
state field is intended to be consumed after the chat turn completes.
"""

from typing import Annotated, Any

from langchain.agents.middleware.types import (
    AgentMiddleware,
    AgentState,
    ContextT,
    OmitFromInput,
    ResponseT,
)
from langchain.tools import ToolRuntime
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langgraph.runtime import Runtime
from langgraph.types import Command
from pydantic import BaseModel
from typing_extensions import NotRequired, override


class PmidsState(AgentState[ResponseT]):
    """State schema for the PMID tracking middleware.

    Type Parameters:
        ResponseT: The type of the structured response. Defaults to `Any`.
    """

    pmids: Annotated[NotRequired[list[str]], OmitFromInput]
    """List of PubMed IDs the agent is currently tracking."""


class WritePmidsInput(BaseModel):
    """Input schema for the `write_pmids` tool."""

    pmids: list[str]


WRITE_PMIDS_TOOL_DESCRIPTION = """Use this tool to maintain the canonical list of PubMed IDs (PMIDs) the agent is tracking for the current session.

Calling this tool REPLACES the entire `pmids` list in agent state with the value you supply. To add new PMIDs, include both the existing PMIDs and the new ones. To remove PMIDs, omit them from the list.

## When to use
- After running `query_pubmed_articles` record the PMIDs of articles you actually used to answer the user.
- When the user explicitly asks you to drop or replace specific PMIDs.
- Whenever the set of relevant PMIDs changes during a multi-step research workflow.

## Rules
- Pass each PMID as a string. Do not include URLs, prefixes (e.g. `PMID:`), or whitespace.
- Deduplicate before calling: each PMID should appear at most once in the list.
- Never call this tool more than once per model turn.
- Do not call this tool with an empty list unless the user explicitly asks you to clear the tracked PMIDs.
"""


def _write_pmids(runtime: ToolRuntime, pmids: list[str]) -> Command[Any]:
    """Replace the tracked PMID list in agent state."""
    return Command(
        update={
            "pmids": pmids,
            "messages": [
                ToolMessage(
                    f"Updated tracked PMIDs to {pmids}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )


async def _awrite_pmids(runtime: ToolRuntime, pmids: list[str]) -> Command[Any]:
    """Replace the tracked PMID list in agent state (async)."""
    return _write_pmids(runtime, pmids)


class PmidsMiddleware(AgentMiddleware[PmidsState[ResponseT], ContextT, ResponseT]):
    """Middleware that adds PMID tracking to an agent.

    Exposes a single `write_pmids` tool that replaces the entire `pmids`
    list in agent state, plus a `pmids` state field that consumers (e.g.
    a frontend reading `stream.values`) can render in real time.

    The pattern follows `TodoListMiddleware` for state and tool wiring,
    but does NOT inject any system prompt: the model relies solely on the
    tool description to know when to call `write_pmids`. The `pmids`
    state field is intended for use after the chat turn completes.
    """

    state_schema = PmidsState  # type: ignore[assignment]

    def __init__(
        self,
        *,
        tool_description: str = WRITE_PMIDS_TOOL_DESCRIPTION,
    ) -> None:
        super().__init__()
        self.tool_description = tool_description

        self.tools = [
            StructuredTool.from_function(
                name="write_pmids",
                description=tool_description,
                func=_write_pmids,
                coroutine=_awrite_pmids,
                args_schema=WritePmidsInput,
                infer_schema=False,
            )
        ]

    @override
    def after_model(
        self, state: PmidsState[ResponseT], runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        """Reject responses that issue multiple parallel `write_pmids` calls."""
        messages = state["messages"]
        if not messages:
            return None

        last_ai_msg = next(
            (msg for msg in reversed(messages) if isinstance(msg, AIMessage)), None
        )
        if not last_ai_msg or not last_ai_msg.tool_calls:
            return None

        write_pmids_calls = [
            tc for tc in last_ai_msg.tool_calls if tc["name"] == "write_pmids"
        ]
        if len(write_pmids_calls) > 1:
            error_messages = [
                ToolMessage(
                    content=(
                        "Error: The `write_pmids` tool should never be called multiple "
                        "times in parallel. Call it only once per model invocation to "
                        "update the PMID list."
                    ),
                    tool_call_id=tc["id"],
                    status="error",
                )
                for tc in write_pmids_calls
            ]
            return {"messages": error_messages}

        return None

    @override
    async def aafter_model(
        self, state: PmidsState[ResponseT], runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        return self.after_model(state, runtime)
