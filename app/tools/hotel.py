import re

from app.data.mock_data import HOTELS
from app.tools.base import ToolInputError

HOTEL_RE = re.compile(r"^H\d{3}$")


def get_hotel_details(hotel_id: str) -> dict:
    hid = hotel_id.strip().upper()
    if not HOTEL_RE.match(hid):
        raise ToolInputError("hotel_id", f"'{hotel_id}' isn't a valid hotel ID (format: H101).")
    if hid not in HOTELS:
        raise ToolInputError("hotel_id", f"I couldn't find hotel {hid}.")
    return {"hotel_id": hid, **HOTELS[hid]}