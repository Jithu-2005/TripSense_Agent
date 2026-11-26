from app.data.mock_data import WEATHER
from app.tools.base import ToolInputError

VALID_DAYS = ("today", "tomorrow", "day_after_tomorrow")


def get_weather(location: str, day: str = "today") -> dict:
    city = location.strip().lower()
    if city not in WEATHER:
        available = ", ".join(c.title() for c in WEATHER)
        raise ToolInputError(
            "location",
            f"I don't have weather data for '{location}'. Available cities: {available}.",
        )
    if day not in VALID_DAYS:
        raise ToolInputError("day", f"Unsupported day '{day}'. Use today, tomorrow or day after tomorrow.")
    return {"location": city.title(), "day": day, **WEATHER[city][day]}