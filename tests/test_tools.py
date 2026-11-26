import pytest

from app.tools.base import ToolInputError
from app.tools.flight import get_flight_status
from app.tools.hotel import get_hotel_details
from app.tools.weather import get_weather


def test_weather_ok():
    assert get_weather("hyderabad")["location"] == "Hyderabad"
    assert get_weather("Delhi", "tomorrow")["day"] == "tomorrow"


def test_weather_unknown_city():
    with pytest.raises(ToolInputError) as e:
        get_weather("Atlantis")
    assert e.value.arg == "location"


def test_flight_ok_and_normalised():
    assert get_flight_status(" f101 ")["status"] == "On time"


@pytest.mark.parametrize("bad", ["hello", "ZZZ", "!!", "ZZ999"])
def test_flight_invalid(bad):
    with pytest.raises(ToolInputError):
        get_flight_status(bad)


def test_hotel_ok_and_invalid():
    assert get_hotel_details("h101")["name"] == "Taj Krishna"
    with pytest.raises(ToolInputError):
        get_hotel_details("101")
    with pytest.raises(ToolInputError):
        get_hotel_details("H999")