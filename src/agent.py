from datetime import datetime
from deepagents.backends import CompositeBackend, StoreBackend, StateBackend
from deepagents import create_deep_agent

from src.llm_models import llm_model
from src.article_agent.prompts import ARTICLE_SYSTEM_PROMPT
from src.article_agent.subagents import research_agent
from src.synopsis_agent.prompts import (
    ROOT_AGENT_SYSTEM_PROMPT,
)
from src.synopsis_agent.subagents import (
    drug_label_agent,
    existing_protocol_agent,
    protocol_sections_agent,
)
from src.tools import generate_image, think_tool, write_output


max_concurrent_research_units = 3
max_researcher_iterations = 3
current_date = datetime.now().strftime("%Y-%m-%d")

synopsis_composite_backend = lambda rt: CompositeBackend(
    default=StateBackend(rt),
    routes={
        "/memories/synopsis": StoreBackend(
            rt, namespace=lambda ctx: ("filesystem-synopsis",)
        ),
    },
)

synopsis_agent = create_deep_agent(
    name="root_agent",
    model=llm_model,
    system_prompt=ROOT_AGENT_SYSTEM_PROMPT,
    tools=[write_output, think_tool],
    subagents=[drug_label_agent, existing_protocol_agent, protocol_sections_agent],
    backend=synopsis_composite_backend,
    memory=["/memories/synopsis/AGENTS.md"],
)

synopsis_agent = synopsis_agent.with_config({"recursion_limit": 500})

article_composite_backend = lambda rt: CompositeBackend(
    default=StateBackend(rt),
    routes={
        "/memories/article": StoreBackend(
            rt, namespace=lambda ctx: ("filesystem-article",)
        ),
    },
)

article_agent = create_deep_agent(
    model=llm_model,
    name="article_root_agent",
    system_prompt=ARTICLE_SYSTEM_PROMPT,
    backend=article_composite_backend,
    subagents=[research_agent],
    tools=[think_tool, generate_image],
)

article_agent = article_agent.with_config({"recursion_limit": 500})

# messages: List[BaseMessage] = []
# messages.append(HumanMessage(USER_INPUT))

# result = agent.invoke({"messages": messages})

# for chunk in agent.stream(
#     {"messages": messages},
#     stream_mode="updates",
#     subgraphs=True,
#     version="v2",
# ):
#     if chunk["type"] == "updates":
#         # Main agent updates (empty namespace)
#         if not chunk["ns"]:
#             for node_name, data in chunk["data"].items():
#                 if node_name == "tools":
#                     # Subagent results returned to main agent
#                     for msg in data.get("messages", []):
#                         if msg.type == "tool":
#                             print(f"\nSubagent complete: {msg.name}")
#                             print(f"  Result: {str(msg.content)[:200]}...")
#                 else:
#                     print(f"[main agent] step: {node_name}")

#         # Subagent updates (non-empty namespace)
#         else:
#             for node_name, data in chunk["data"].items():
#                 print(f"  [{chunk['ns'][0]}] step: {node_name}")

# print()

# for chunk in agent.stream(
#     {"messages": messages},
#     stream_mode="messages",
#     subgraphs=True,
#     version="v2",
# ):
#     if chunk["type"] == "messages":
#         token, metadata = chunk["data"]

#         # Identify source: "main" or the subagent namespace segment
#         is_subagent = any(s.startswith("tools:") for s in chunk["ns"])
#         source = (
#             next((s for s in chunk["ns"] if s.startswith("tools:")), "main")
#             if is_subagent
#             else "main"
#         )

#         # Tool call chunks (streaming tool invocations)
#         if token.tool_call_chunks:
#             for tc in token.tool_call_chunks:
#                 if tc.get("name"):
#                     print(f"\n[{source}] Tool call: {tc['name']}")
#                 # Args stream in chunks - write them incrementally
#                 if tc.get("args"):
#                     print(tc["args"], end="", flush=True)

#         # Tool results
#         if token.type == "tool":
#             print(
#                 f"\n[{source}] Tool result [{token.name}]: {str(token.content)[:150]}"
#             )

#         # Regular AI content (skip tool call messages)
#         if token.type == "ai" and token.content and not token.tool_call_chunks:
#             print(token.content, end="", flush=True)

# print()
