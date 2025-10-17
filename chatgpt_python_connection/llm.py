import os

from openai import OpenAI

# Keys default to sample values so the script still runs.
OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    "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",
)
A4F_API_KEY = os.getenv(
    "A4F_API_KEY",
    "ddc-a4f-5ccc37b0cfac450e920c6f3184dd3037",
)

openrouter_client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

a4f_client = OpenAI(
    api_key=A4F_API_KEY,
    base_url="https://api.a4f.co/v1",
)

DEFAULT_OPENROUTER_MODEL = "meta-llama/llama-4-maverick:free"
DEFAULT_A4F_MODEL = os.getenv("A4F_DEFAULT_MODEL") or "provider-3/gpt-4o-mini"

SERVICES = {
    "openrouter": {
        "name": "openrouter",
        "client": openrouter_client,
        "default_model": DEFAULT_OPENROUTER_MODEL,
    },
    "a4f": {
        "name": "a4f",
        "client": a4f_client,
        "default_model": DEFAULT_A4F_MODEL,
    },
}


def _chat(client, model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


def get_service(service_name):
    if service_name not in SERVICES:
        raise ValueError(f"Unsupported service: {service_name}")

    info = SERVICES[service_name]

    def generate_from_service(prompt, model=None):
        return generate(prompt, service_name, model)

    return {
        "name": info["name"],
        "default_model": info["default_model"],
        "generate": generate_from_service,
    }


def generate(prompt, service="openrouter", model=None):
    if service not in SERVICES:
        raise ValueError(f"Unsupported service: {service}")

    info = SERVICES[service]
    model_to_use = model or info["default_model"]
    return _chat(info["client"], model_to_use, prompt)


def llm_generate_text(prompt, service="openrouter", model=None):
    """
    Backwards-compatible helper to generate text using a named service.

    Args:
        prompt: Text to send to the language model.
        service: Service alias (case insensitive). Supports "openrouter",
                 "a4f", and "openai" (alias of openrouter).
        model: Optional model override.
    """

    normalized = (service or "openrouter").strip().lower()
    if normalized == "openai":
        normalized = "openrouter"

    return generate(prompt, service=normalized, model=model)


# Optional reference lists.
OPENROUTER_FREE = [
    "meta-llama/llama-4-maverick:free",
    "meta-llama/llama-3.2-3b-instruct:free",
]

OPENROUTER_PAID = [
    "openai/gpt-3.5-turbo",
    "openai/gpt-4o-mini",
    "openai/gpt-4",
]

A4F_MODELS = [
    "provider-1/chatgpt-4o-latest",
    "openai/gpt-4o",
    "anthropic/claude-3.5-sonnet",
]
