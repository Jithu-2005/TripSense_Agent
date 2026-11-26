import os

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME: str = os.getenv("LLM_MODEL", "groq:openai/gpt-oss-20b")
CHECKPOINT_DB: str = os.getenv("CHECKPOINT_DB", "")  # "" => in-memory