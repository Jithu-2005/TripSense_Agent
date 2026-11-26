from typing import Annotated, Any

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    parsed: dict[str, Any]
    pending: list[dict]          # [{tool, args, missing, error?}]
    last_args: dict[str, dict]   # last successful args per tool
    ready_calls: list[dict]      # [{tool, args}]
    results: list[dict]          # [{tool, args, output}]
    needs_input: list[dict]
    unsupported: bool