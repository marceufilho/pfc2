"""The one adapter to the language-model service used by `--prove`.

One request per call, no retries, a JSON-schema reply. The key is read from the environment only and
never appears in an argument, a log or an error message. Whatever comes back is untrusted text: the
caller parses it as data and the checker decides.
"""

import os
import re
from dataclasses import dataclass

from openai import APIError, OpenAI, omit

from pfc2.core.config import MAX_PROMPT_BYTES, MAX_PROPOSAL_BYTES, OPENAI_KEY_ENV

MODEL_ENV = "PFC2_MODEL"
DEFAULT_MODEL = "gpt-6-astra"
BASE_URL = "https://api.openai.com/v1"
TIMEOUT_SECONDS = 60
OUTPUT_TOKENS = 2048
_MODEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,99}")
_SCHEMA = {
    "type": "object",
    "properties": {"invariants": {"type": "array", "items": {"type": "string"}}},
    "required": ["invariants"],
    "additionalProperties": False,
}


@dataclass(frozen=True)
class Reply:
    text: str
    model: str


def model() -> str:
    """The configured model: `PFC2_MODEL`, or the default."""
    name = os.environ.get(MODEL_ENV, DEFAULT_MODEL)
    if not _MODEL.fullmatch(name):
        raise ValueError(f"{MODEL_ENV} is not a model name")
    return name


def ask(prompt: str, *, client: OpenAI | None = None) -> Reply:
    """Exactly one HTTP attempt; every failure is a ValueError that hides the service's message."""
    if not prompt or len(prompt.encode("utf-8")) > MAX_PROMPT_BYTES:
        raise ValueError("empty or oversized prompt")
    name = model()
    if client is None:
        key = os.environ.get(OPENAI_KEY_ENV)
        if not key or any(character.isspace() for character in key):
            raise ValueError(f"configure {OPENAI_KEY_ENV} in the environment; never pass it as an argument")
        with OpenAI(api_key=key, base_url=BASE_URL, max_retries=0, timeout=TIMEOUT_SECONDS) as owned:
            return ask(prompt, client=owned)
    try:
        response = client.responses.create(
            model=name,
            input=prompt,
            store=False,
            temperature=omit,
            reasoning={"effort": "low"},
            max_output_tokens=OUTPUT_TOKENS,
            text={"format": {"type": "json_schema", "name": "loop_invariants", "strict": True, "schema": _SCHEMA}},
        )
        if response.status != "completed":
            raise ValueError("the model's response was incomplete or refused")
        text, answered = response.output_text, response.model
    except (AttributeError, TypeError):
        raise ValueError("malformed response from the model service") from None
    except APIError as error:
        # SDK messages can carry response bodies, prompts or credentials.
        raise ValueError(f"the request failed ({type(error).__name__}); check account access and limits") from None
    if not isinstance(text, str) or not text.strip() or len(text.encode("utf-8")) > MAX_PROPOSAL_BYTES:
        raise ValueError("empty or oversized response from the model")
    return Reply(text, answered if isinstance(answered, str) else name)
