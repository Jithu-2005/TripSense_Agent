from typing import Callable

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import MODEL_NAME
from app.prompts import SYSTEM_PROMPT
from app.schemas import ParsedRequest

# A "parser" is any callable (user_text, context) -> ParsedRequest.
# Production uses the LLM; tests inject a scripted fake.
Parser = Callable[[str, str], ParsedRequest]


def make_llm_parser(model_name: str = MODEL_NAME) -> Parser:
    llm = init_chat_model(model_name, temperature=0).with_structured_output(ParsedRequest)

    def parse(text: str, context: str) -> ParsedRequest:
        result = llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=f"CONTEXT:\n{context}\n\nUSER MESSAGE:\n{text}"),
            ]
        )
        return result if isinstance(result, ParsedRequest) else ParsedRequest(**result)

    return parse