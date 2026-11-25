import os

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME: str = os.getenv("LLM_MODEL", "openai:gpt-4o-mini")
CHECKPOINT_DB: str = os.getenv("CHECKPOINT_DB", "")  # "" => in-memory