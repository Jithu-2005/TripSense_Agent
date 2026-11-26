from app.graph import chat

T = "thread-1"


def test_full_acceptance_flow(graph):
    # 1. weather executes
    r = chat(graph, T, "What is the weather in Hyderabad?")
    assert "Weather in Hyderabad (today)" in r

    # 2. missing flight number -> ask
    r = chat(graph, T, "Check my flight status")
    assert "flight number" in r.lower()

    # 3. slot filled on next turn -> executes
    r = chat(graph, T, "My flight number is F101")
    assert "Flight F101" in r and "On time" in r

    # 4. multi-intent: hotel runs, weather asks for city
    r = chat(graph, T, "Check the weather and hotel H101")
    assert "Taj Krishna" in r
    assert "which city" in r.lower()

    # 5. follow-up reuses previous weather location
    r = chat(graph, T, "What about tomorrow?")
    assert "Hyderabad (tomorrow)" in r

    # 6. unsupported
    r = chat(graph, T, "Tell me stock prices")
    assert "can't help" in r.lower()


def test_multi_intent_all_execute(graph):
    r = chat(graph, "t2", "Weather in Delhi and hotel H103 and flight AI202")
    assert "Delhi" in r and "Leela" in r and "AI202" in r


def test_invalid_flight_reasks_and_recovers(graph):
    r = chat(graph, "t3", "Flight ZZ999")
    assert "couldn't find" in r.lower()
    r = chat(graph, "t3", "My flight number is ZZZ")
    assert "valid flight number" in r.lower()


def test_invalid_city(graph):
    r = chat(graph, "t4", "Weather in Atlantis")
    assert "don't have weather data" in r.lower()


def test_followup_without_context_asks_city(graph):
    r = chat(graph, "t5", "What about tomorrow?")   # no prior weather in this thread
    assert "which city" in r.lower()


def test_threads_are_isolated(graph):
    chat(graph, "a", "What is the weather in Hyderabad?")
    r = chat(graph, "b", "What about tomorrow?")      # thread b has no context
    assert "which city" in r.lower()


def test_pending_weather_completed_by_city(graph):
    chat(graph, "t6", "Check the weather and hotel H101")
    r = chat(graph, "t6", "It is Mumbai")
    assert "Mumbai" in r