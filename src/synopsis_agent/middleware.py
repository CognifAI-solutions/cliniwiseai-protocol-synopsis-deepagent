"""Synopsis status tracking middleware for the synopsis agent.

Adds a custom `synopsis_status` field to the agent state and exposes a
`write_synopsis_status` tool that replaces the boolean status, mirroring the
`write_todos` pattern documented at:
https://docs.langchain.com/oss/python/deepagents/frontend/todo-list#custom-state-beyond-todos

The middleware does NOT inject anything into the system prompt. The agent
discovers `write_synopsis_status` purely through its tool description, and the
`synopsis_status` state field is intended to be consumed after the chat turn
completes.
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


class SynopsisStatusState(AgentState[ResponseT]):
    """State schema for the synopsis status tracking middleware.

    Type Parameters:
        ResponseT: The type of the structured response. Defaults to `Any`.
    """

    synopsis_status: Annotated[NotRequired[bool], OmitFromInput]
    """True if the protocol synopsis is complete, False if it is incomplete or being revised."""


class WriteSynopsisStatusInput(BaseModel):
    """Input schema for the `write_synopsis_status` tool."""

    synopsis_status: bool


WRITE_SYNOPSIS_STATUS_TOOL_DESCRIPTION = """Use this tool to maintain the status of the protocol synopsis completion.

Calling this tool REPLACES the `synopsis_status` field in agent state with the value you supply.

## When to use
- After the protocol synopsis is generated and returned to the user.
- When the user explicitly asks you to change the status of the protocol synopsis.
- Whenever the status of the protocol synopsis changes during a multi-step workflow.

## Rules
- Pass the status as a boolean. True if the protocol synopsis is complete, False if it is incomplete or being revised.
- Never call this tool more than once per model turn.
- Do not call this tool with an empty boolean value unless the user explicitly asks you to clear the status of the protocol synopsis.
"""


def _write_synopsis_status(
    runtime: ToolRuntime, synopsis_status: bool
) -> Command[Any]:
    """Replace the tracked synopsis status in agent state."""
    return Command(
        update={
            "synopsis_status": synopsis_status,
            "messages": [
                ToolMessage(
                    f"Updated synopsis status to {synopsis_status}",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )


async def _awrite_synopsis_status(
    runtime: ToolRuntime, synopsis_status: bool
) -> Command[Any]:
    """Replace the tracked synopsis status in agent state (async)."""
    return _write_synopsis_status(runtime, synopsis_status)


class SynopsisStatusMiddleware(
    AgentMiddleware[SynopsisStatusState[ResponseT], ContextT, ResponseT]
):
    """Middleware that adds synopsis status tracking to an agent.

    Exposes a single `write_synopsis_status` tool that replaces the
    `synopsis_status` boolean in agent state, plus a `synopsis_status` state
    field that consumers (e.g. a frontend reading `stream.values`) can render
    in real time.

    The pattern follows `TodoListMiddleware` for state and tool wiring,
    but does NOT inject any system prompt: the model relies solely on the
    tool description to know when to call `write_synopsis_status`. The
    `synopsis_status` state field is intended for use after the chat turn
    completes.
    """

    state_schema = SynopsisStatusState  # type: ignore[assignment]

    def __init__(
        self,
        *,
        tool_description: str = WRITE_SYNOPSIS_STATUS_TOOL_DESCRIPTION,
    ) -> None:
        super().__init__()
        self.tool_description = tool_description

        self.tools = [
            StructuredTool.from_function(
                name="write_synopsis_status",
                description=tool_description,
                func=_write_synopsis_status,
                coroutine=_awrite_synopsis_status,
                args_schema=WriteSynopsisStatusInput,
                infer_schema=False,
            )
        ]

    @override
    def before_agent(
        self, state: SynopsisStatusState[ResponseT], runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        """Seed `synopsis_status` to False on the first turn if unset."""
        if state.get("synopsis_status") is None:
            return {"synopsis_status": False}
        return None

    @override
    async def abefore_agent(
        self, state: SynopsisStatusState[ResponseT], runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        return self.before_agent(state, runtime)

    @override
    def after_model(
        self, state: SynopsisStatusState[ResponseT], runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        """Reject responses that issue multiple parallel `write_synopsis_status` calls."""
        messages = state["messages"]
        if not messages:
            return None

        last_ai_msg = next(
            (msg for msg in reversed(messages) if isinstance(msg, AIMessage)), None
        )
        if not last_ai_msg or not last_ai_msg.tool_calls:
            return None

        write_synopsis_status_calls = [
            tc
            for tc in last_ai_msg.tool_calls
            if tc["name"] == "write_synopsis_status"
        ]
        if len(write_synopsis_status_calls) > 1:
            error_messages = [
                ToolMessage(
                    content=(
                        "Error: The `write_synopsis_status` tool should never be "
                        "called multiple times in parallel. Call it only once per "
                        "model invocation to update the synopsis status."
                    ),
                    tool_call_id=tc["id"],
                    status="error",
                )
                for tc in write_synopsis_status_calls
            ]
            return {"messages": error_messages}

        return None

    @override
    async def aafter_model(
        self, state: SynopsisStatusState[ResponseT], runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        return self.after_model(state, runtime)
