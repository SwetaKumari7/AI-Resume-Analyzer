import requests


OLLAMA_HOST = "http://127.0.0.1:11434"
DEFAULT_MODEL = "gemma3:4b"


def generate_local_response(
    prompt: str,
    system_instruction: str = "",
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Generate an AI response using a local Ollama model.

    The request is sent to Ollama running on the
    user's own computer.
    """

    messages = []

    if system_instruction:
        messages.append(
            {
                "role": "system",
                "content": system_instruction,
            }
        )

    messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    response = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.2,
            },
        },
        timeout=300,
    )

    response.raise_for_status()

    data = response.json()

    message = data.get(
        "message",
        {},
    )

    answer = message.get(
        "content",
        "",
    )

    if not answer:
        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return answer.strip()