import re

from app.data.mock_data import FLIGHTS
from app.tools.base import ToolInputError

FLIGHT_RE = re.compile(r"^[A-Z0-9]{2,3}\d{2,4}$")


def get_flight_status(flight_number: str) -> dict:
    fn = flight_number.strip().upper().replace(" ", "")
    if not FLIGHT_RE.match(fn):
        raise ToolInputError(
            "flight_number",
            f"'{flight_number}' doesn't look like a valid flight number (e.g. F101, AI202).",
        )
    if fn not in FLIGHTS:
        raise ToolInputError("flight_number", f"I couldn't find flight {fn}.")
    return {"flight_number": fn, **FLIGHTS[fn]}