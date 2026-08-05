import logging
import time

from ollama import chat
from config.settings import LLM_MODEL

logger = logging.getLogger(__name__)


def generate_answer(prompt):

    start = time.perf_counter()

    response = chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    generation_time_ms = round((time.perf_counter() - start) * 1000, 2)

    logger.info(
        "generation_completed",
        extra={
            "event": "generation_completed",
            "generation_time_ms": generation_time_ms,
        },
    )

    return response.message.content