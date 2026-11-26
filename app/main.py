import uuid

from app.graph import build_graph, chat


def main() -> None:
    graph = build_graph()
    thread_id = str(uuid.uuid4())
    print("Travel assistant ready (weather / flight status / hotel details). Type 'exit' to quit.\n")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in {"exit", "quit"}:
            break
        if user:
            print(f"Bot: {chat(graph, thread_id, user)}\n")


if __name__ == "__main__":
    main()