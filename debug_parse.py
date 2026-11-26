from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import MODEL_NAME
from app.prompts import SYSTEM_PROMPT
from app.schemas import ParsedRequest

base = init_chat_model(MODEL_NAME, temperature=0)
msgs = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content="CONTEXT:\n(no prior context)\n\nUSER MESSAGE:\nwhat is the weather in hyderabad?"),
]
for method in ("json_schema", "function_calling"):
    for i in range(3):                      # run 3 times to catch flaky output
        try:
            print(method, i, base.with_structured_output(ParsedRequest, method=method).invoke(msgs))
        except Exception as e:
            print(method, i, "ERROR:", str(e)[:150])