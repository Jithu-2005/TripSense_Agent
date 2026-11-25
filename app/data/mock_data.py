"""Mock data sources. Replace with real APIs/DB later without touching the agent."""

WEATHER = {
    "hyderabad": {
        "today": {"condition": "Partly cloudy", "temp_c": 29, "humidity": 62},
        "tomorrow": {"condition": "Light rain", "temp_c": 26, "humidity": 78},
        "day_after_tomorrow": {"condition": "Sunny", "temp_c": 31, "humidity": 55},
    },
    "bengaluru": {
        "today": {"condition": "Cloudy", "temp_c": 24, "humidity": 70},
        "tomorrow": {"condition": "Showers", "temp_c": 22, "humidity": 82},
        "day_after_tomorrow": {"condition": "Partly cloudy", "temp_c": 25, "humidity": 68},
    },
    "mumbai": {
        "today": {"condition": "Humid and sunny", "temp_c": 32, "humidity": 80},
        "tomorrow": {"condition": "Thunderstorms", "temp_c": 29, "humidity": 88},
        "day_after_tomorrow": {"condition": "Cloudy", "temp_c": 30, "humidity": 79},
    },
    "delhi": {
        "today": {"condition": "Hazy", "temp_c": 27, "humidity": 45},
        "tomorrow": {"condition": "Clear", "temp_c": 28, "humidity": 40},
        "day_after_tomorrow": {"condition": "Sunny", "temp_c": 30, "humidity": 38},
    },
    "chennai": {
        "today": {"condition": "Hot and humid", "temp_c": 33, "humidity": 75},
        "tomorrow": {"condition": "Partly cloudy", "temp_c": 32, "humidity": 72},
        "day_after_tomorrow": {"condition": "Light rain", "temp_c": 29, "humidity": 84},
    },
}

FLIGHTS = {
    "F101": {"status": "On time", "origin": "Hyderabad", "destination": "Delhi",
             "departure": "10:30", "arrival": "12:45", "gate": "B12"},
    "F102": {"status": "Delayed by 40 min", "origin": "Mumbai", "destination": "Hyderabad",
             "departure": "14:10", "arrival": "16:00", "gate": "A07"},
    "AI202": {"status": "Boarding", "origin": "Delhi", "destination": "Bengaluru",
              "departure": "09:15", "arrival": "11:55", "gate": "C03"},
    "6E303": {"status": "Cancelled", "origin": "Chennai", "destination": "Mumbai",
              "departure": "18:00", "arrival": "20:10", "gate": "-"},
}

HOTELS = {
    "H101": {"name": "Taj Krishna", "city": "Hyderabad", "rating": 5,
             "price_per_night_inr": 12500, "amenities": ["Pool", "Spa", "Free Wi-Fi", "Gym"]},
    "H102": {"name": "Novotel HICC", "city": "Hyderabad", "rating": 4,
             "price_per_night_inr": 8200, "amenities": ["Pool", "Free Wi-Fi", "Restaurant"]},
    "H103": {"name": "The Leela Palace", "city": "Bengaluru", "rating": 5,
             "price_per_night_inr": 15000, "amenities": ["Spa", "Free Wi-Fi", "Airport shuttle"]},
}