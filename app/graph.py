import sqlite3
from typing import Optional

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app import config
from app.llm import Parser, make_llm_parser
from app.nodes import execute, make_understand_node, plan, respond, route_after_plan
from app.state import AgentState


def make_checkpointer() -> BaseCheckpointSaver:
    if config.CHECKPOINT_DB:
        from langgraph.checkpoint.sqlite import SqliteSaver

        conn = sqlite3.connect(config.CHECKPOINT_DB, check_same_thread=False)
        return SqliteSaver(conn)
    return MemorySaver()


def build_graph(parser: Optional[Parser] = None, checkpointer: Optional[BaseCheckpointSaver] = None):
    parser = parser or make_llm_parser()
    checkpointer = checkpointer or make_checkpointer()

    g = StateGraph(AgentState)
    g.add_node("understand", make_understand_node(parser))
    g.add_node("plan", plan)
    g.add_node("execute", execute)
    g.add_node("respond", respond)

    g.add_edge(START, "understand")
    g.add_edge("understand", "plan")
    g.add_conditional_edges("plan", route_after_plan, {"execute": "execute", "respond": "respond"})
    g.add_edge("execute", "respond")
    g.add_edge("respond", END)

    return g.compile(checkpointer=checkpointer)


def chat(graph, thread_id: str, message: str) -> str:
    """Send one user message; conversation state is restored via thread_id."""
    out = graph.invoke(
        {"messages": [("user", message)]},
        config={"configurable": {"thread_id": thread_id}},
    )
    return out["messages"][-1].content