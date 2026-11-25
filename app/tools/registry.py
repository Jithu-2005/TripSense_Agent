"""Single source of truth for tools. Adding a tool = add one ToolSpec here
(+ schema literal in schemas.py + formatter in nodes.py)."""
from dataclasses import dataclass, field
from typing import Callable

from app.tools.flight import get_flight_status
from app.tools.hotel import get_hotel_details
from app.tools.weather import get_weather


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    func: Callable[..., dict]
    required: tuple[str, ...]
    defaults: dict = field(default_factory=dict)
    questions: dict = field(default_factory=dict)  # arg -> clarification question


REGISTRY: dict[str, ToolSpec] = {
    "get_weather": ToolSpec(
        name="get_weather",
        description="Weather for a city (today / tomorrow / day after tomorrow).",
        func=get_weather,
        required=("location",),
        defaults={"day": "today"},
        questions={"location": "Which city would you like the weather for?"},
    ),
    "get_flight_status": ToolSpec(
        name="get_flight_status",
        description="Status of a flight by flight number.",
        func=get_flight_status,
        required=("flight_number",),
        questions={"flight_number": "What's your flight number? (e.g. F101)"},
    ),
    "get_hotel_details": ToolSpec(
        name="get_hotel_details",
        description="Hotel information by hotel ID.",
        func=get_hotel_details,
        required=("hotel_id",),
        questions={"hotel_id": "What's the hotel ID? (e.g. H101)"},
    ),
}