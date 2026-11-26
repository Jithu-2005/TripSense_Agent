import logging
import uuid

import streamlit as st

from app.graph import build_graph, chat

log = logging.getLogger(__name__)

st.set_page_config(page_title="TripSense Agent", page_icon="✈️")
st.title("✈️ TripSense Agent")
st.caption("Ask about weather, flight status or hotel details.")

EXAMPLES = [
    "What is the weather in Hyderabad?",
    "Check my flight status",
    "My flight number is F101",
    "Check the weather and hotel H101",
    "What about tomorrow?",
    "Tell me stock prices",
]
ERROR_REPLY = "⚠️ Sorry, something went wrong while processing that. Please try again."


@st.cache_resource
def get_graph():
    return build_graph()          # built once, shared across reruns


graph = get_graph()


def new_chat():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.history = []


def render(text: str) -> None:
    # Streamlit markdown ignores single newlines; two trailing spaces force a line break.
    st.markdown(text.replace("\n", "  \n"))


if "thread_id" not in st.session_state:
    new_chat()

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.header("Controls")
    if st.button("🗑 New conversation", use_container_width=True):
        new_chat()
        st.rerun()

    st.subheader("Try these")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state.queued = ex

    show_state = st.toggle("Show agent state")

# ------------------------------------------------------------------- chat
for role, text in st.session_state.history:
    with st.chat_message(role):
        render(text)

prompt = st.chat_input("Ask about weather, flights or hotels...")
prompt = prompt or st.session_state.pop("queued", None)

if prompt:
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                reply = chat(graph, st.session_state.thread_id, prompt)
        except Exception:
            log.exception("chat turn failed")
            reply = ERROR_REPLY
        render(reply)
    st.session_state.history.append(("assistant", reply))

# ------------------------------------------------- optional: state viewer
if show_state:
    values = graph.get_state(
        {"configurable": {"thread_id": st.session_state.thread_id}}
    ).values
    st.sidebar.json(
        {
            "pending": values.get("pending", []),
            "last_args": values.get("last_args", {}),
            "parsed": values.get("parsed", {}),
        }
    )