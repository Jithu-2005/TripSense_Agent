import pytest
from langgraph.checkpoint.memory import MemorySaver

from app.graph import build_graph
from app.schemas import IntentItem, ParsedRequest

SCRIPT = {
    "What is the weather in Hyderabad?": [IntentItem(intent="get_weather", location="Hyderabad")],
    "Check my flight status": [IntentItem(intent="get_flight_status")],
    "My flight number is F101": [IntentItem(intent="get_flight_status", flight_number="F101")],
    "Check the weather and hotel H101": [
        IntentItem(intent="get_weather"),
        IntentItem(intent="get_hotel_details", hotel_id="H101"),
    ],
    "What about tomorrow?": [
        IntentItem(intent="get_weather", day="tomorrow", inherit_context=True)
    ],
    "Tell me stock prices": [IntentItem(intent="unsupported")],
    "My flight number is ZZZ": [IntentItem(intent="get_flight_status", flight_number="ZZZ")],
    "Weather in Atlantis": [IntentItem(intent="get_weather", location="Atlantis")],
    "Flight ZZ999": [IntentItem(intent="get_flight_status", flight_number="ZZ999")],
    "Weather in Delhi and hotel H103 and flight AI202": [
        IntentItem(intent="get_weather", location="Delhi"),
        IntentItem(intent="get_hotel_details", hotel_id="H103"),
        IntentItem(intent="get_flight_status", flight_number="AI202"),
    ],
    "It is Mumbai": [IntentItem(intent="get_weather", location="Mumbai")],
}


def scripted_parser(text: str, context: str) -> ParsedRequest:
    return ParsedRequest(intents=SCRIPT[text])


@pytest.fixture
def graph():
    return build_graph(parser=scripted_parser, checkpointer=MemorySaver())