from langchain_core.messages import AIMessage, HumanMessage

from app.llm import Parser
from app.schemas import ParsedRequest
from app.state import AgentState
from app.tools.base import ToolInputError
from app.tools.registry import REGISTRY

UNSUPPORTED_REPLY = (
    "Sorry, I can't help with that. I can check **weather**, **flight status** "
    "and **hotel details**."
)


# ----------------------------------------------------------------- helpers
def _build_context(state: AgentState) -> str:
    lines = []
    for p in state.get("pending", []):
        lines.append(
            f"- Assistant is WAITING for {p['missing']} for tool {p['tool']} (already known: {p['args']})"
        )
    for tool, args in state.get("last_args", {}).items():
        lines.append(f"- Last successful {tool} call used: {args}")
    recent = state.get("messages", [])[-7:-1]
    for m in recent:
        role = "User" if isinstance(m, HumanMessage) else "Assistant"
        lines.append(f"{role}: {m.content}")
    return "\n".join(lines) or "(no prior context)"


def _fmt_weather(o: dict) -> str:
    day = o["day"].replace("_", " ")
    return f"🌤 Weather in {o['location']} ({day}): {o['condition']}, {o['temp_c']}°C, humidity {o['humidity']}%."


def _fmt_flight(o: dict) -> str:
    return (
        f"✈️ Flight {o['flight_number']}: {o['status']}. {o['origin']} → {o['destination']}, "
        f"departs {o['departure']}, arrives {o['arrival']}, gate {o['gate']}."
    )


def _fmt_hotel(o: dict) -> str:
    return (
        f"🏨 {o['name']} ({o['hotel_id']}), {o['city']} — {o['rating']}★, "
        f"₹{o['price_per_night_inr']:,}/night. Amenities: {', '.join(o['amenities'])}."
    )


FORMATTERS = {
    "get_weather": _fmt_weather,
    "get_flight_status": _fmt_flight,
    "get_hotel_details": _fmt_hotel,
}


# ------------------------------------------------------------------- nodes
def make_understand_node(parser: Parser):
    def understand(state: AgentState) -> dict:
        text = state["messages"][-1].content
        parsed = parser(text, _build_context(state))
        return {"parsed": parsed.model_dump()}

    return understand


def plan(state: AgentState) -> dict:
    """Deterministic planning: merge pending/context, validate required args."""
    parsed = ParsedRequest(**state["parsed"])
    pending = {p["tool"]: p for p in state.get("pending", [])}
    last_args = state.get("last_args", {})

    ready, needs, unsupported = [], [], False

    for item in parsed.intents:
        if item.intent == "unsupported":
            unsupported = True
            continue

        spec = REGISTRY[item.intent]
        merged = dict(pending.pop(item.intent, {}).get("args", {}))   # args from earlier turns
        merged.update(item.args())                                     # new args win
        if item.inherit_context:
            for k, v in last_args.get(item.intent, {}).items():
                merged.setdefault(k, v)                                # fill gaps from history
        for k, v in spec.defaults.items():
            merged.setdefault(k, v)

        missing = [r for r in spec.required if not merged.get(r)]
        if missing:
            needs.append({"tool": item.intent, "args": merged, "missing": missing})
        else:
            ready.append({"tool": item.intent, "args": merged})

    if not parsed.intents:
        unsupported = True

    return {"ready_calls": ready, "needs_input": needs, "unsupported": unsupported}


def execute(state: AgentState) -> dict:
    results = []
    needs = list(state.get("needs_input", []))
    last_args = dict(state.get("last_args", {}))

    for call in state.get("ready_calls", []):
        spec = REGISTRY[call["tool"]]
        try:
            output = spec.func(**call["args"])
            results.append({"tool": call["tool"], "args": call["args"], "output": output})
            last_args[call["tool"]] = dict(call["args"])
        except ToolInputError as err:
            bad_args = {k: v for k, v in call["args"].items() if k != err.arg}
            needs.append(
                {"tool": call["tool"], "args": bad_args, "missing": [err.arg], "error": err.message}
            )

    return {"results": results, "needs_input": needs, "last_args": last_args}


def respond(state: AgentState) -> dict:
    parts = [FORMATTERS[r["tool"]](r["output"]) for r in state.get("results", [])]

    for n in state.get("needs_input", []):
        arg = n["missing"][0]
        question = REGISTRY[n["tool"]].questions.get(arg, f"Please provide {arg}.")
        parts.append(f"⚠️ {n['error']} {question}" if n.get("error") else question)

    if state.get("unsupported"):
        parts.append(UNSUPPORTED_REPLY)

    reply = "\n".join(parts) or UNSUPPORTED_REPLY
    return {
        "messages": [AIMessage(content=reply)],
        "pending": state.get("needs_input", []),   # persisted -> next turn can complete it
    }


def route_after_plan(state: AgentState) -> str:
    return "execute" if state.get("ready_calls") else "respond"