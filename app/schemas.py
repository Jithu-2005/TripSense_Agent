from typing import Literal, Optional

from pydantic import BaseModel, Field

IntentName = Literal["get_weather", "get_flight_status", "get_hotel_details", "unsupported"]
ARG_FIELDS = ("location", "day", "flight_number", "hotel_id")


class IntentItem(BaseModel):
    """One user intent. Arguments are flat optional fields (works with strict
    structured-output modes that dislike free-form dicts)."""

    intent: IntentName = Field(description="Which tool the user wants, or 'unsupported'.")
    location: Optional[str] = Field(None, description="City name for weather.")
    day: Optional[Literal["today", "tomorrow", "day_after_tomorrow"]] = Field(
        None, description="Day for weather. Only set if the user mentioned it."
    )
    flight_number: Optional[str] = Field(None, description="Flight number such as F101.")
    hotel_id: Optional[str] = Field(None, description="Hotel ID such as H101.")
    inherit_context: bool = Field(
        False,
        description="True ONLY for follow-ups that rely on earlier context "
        "(e.g. 'What about tomorrow?', 'and for Delhi?').",
    )

    def args(self) -> dict:
        return {k: getattr(self, k) for k in ARG_FIELDS if getattr(self, k)}


class ParsedRequest(BaseModel):
    intents: list[IntentItem] = Field(
        default_factory=list,
        description="All intents in the message. Multi-intent messages return several items.",
    )