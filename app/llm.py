import logging
from typing import Callable

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import MODEL_NAME
from app.prompts import SYSTEM_PROMPT
from app.schemas import ParsedRequest

log = logging.getLogger(__name__)

Parser = Callable[[str, str], ParsedRequest]


def make_llm_parser(model_name: str = MODEL_NAME) -> Parser:
    base = init_chat_model(model_name, temperature=0)

    # (method, attempts). function_calling is reliable on this model but occasionally
    # raises "Unknown tool type: functions.ParsedRequest", so it is retried.
    # json_schema returned empty intents for every request on gpt-oss-20b, so it is
    # only a last-resort fallback and its empty results are never trusted.
    plan = [("function_calling", 3), ("json_schema", 1)]
    runnables = []
    for method, attempts in plan:
        try:
            runnables.append((method, attempts, base.with_structured_output(ParsedRequest, method=method)))
        except Exception as exc:
            log.warning("structured output method %s unavailable: %s", method, exc)
    if not runnables:
        raise RuntimeError("No structured-output method is supported by this model.")

    def parse(text: str, context: str) -> ParsedRequest:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"CONTEXT:\n{context}\n\nUSER MESSAGE:\n{text}"),
        ]
        last_exc = None
        for idx, (method, attempts, runnable) in enumerate(runnables):
            is_primary = idx == 0
            for attempt in range(1, attempts + 1):
                try:
                    result = runnable.invoke(messages)
                    result = result if isinstance(result, ParsedRequest) else ParsedRequest(**result)
                    if result.intents:
                        return result
                    if is_primary:
                        return result            # model genuinely found no intent
                    log.warning("empty intents from fallback %s for %r; ignoring", method, text)
                except Exception as exc:
                    last_exc = exc
                    log.warning("parse failed (%s, attempt %d/%d): %s", method, attempt, attempts, exc)
        raise RuntimeError("Could not understand the request.") from last_exc

    return parse