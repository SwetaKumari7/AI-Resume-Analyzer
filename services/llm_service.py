import os
import time

from dotenv import load_dotenv

from services.local_llm_service import (
    generate_local_response,
)


load_dotenv()


LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama",
).lower()

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "gemma3:4b",
)


def generate_response(
    prompt: str,
    system_instruction: str = "",
    max_retries: int = 3,
) -> str:
    """
    Generate an AI response.

    Ollama is the default provider.
    Gemini remains available as an optional
    cloud provider.
    """

    if LLM_PROVIDER == "ollama":

        return generate_local_response(
            prompt=prompt,
            system_instruction=system_instruction,
            model=OLLAMA_MODEL,
        )

    if LLM_PROVIDER == "gemini":

        return _generate_gemini_response(
            prompt=prompt,
            system_instruction=system_instruction,
            max_retries=max_retries,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}. "
        "Use 'ollama' or 'gemini'."
    )


def _generate_gemini_response(
    prompt: str,
    system_instruction: str = "",
    max_retries: int = 3,
) -> str:
    """
    Optional Gemini implementation.
    """

    from google import genai

    api_key = os.getenv(
        "GOOGLE_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GOOGLE_API_KEY is missing."
        )

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash",
    )

    client = genai.Client(
        api_key=api_key
    )

    if system_instruction:

        full_prompt = (
            f"SYSTEM INSTRUCTION:\n"
            f"{system_instruction}\n\n"
            f"USER REQUEST:\n"
            f"{prompt}"
        )

    else:

        full_prompt = prompt

    last_error = None

    for attempt in range(
        1,
        max_retries + 1,
    ):

        try:

            response = (
                client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                )
            )

            return response.text or ""

        except Exception as error:

            last_error = error

            error_text = str(error)

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                if attempt < max_retries:

                    wait_seconds = attempt * 3

                    print(
                        "Gemini temporarily unavailable. "
                        f"Retrying in {wait_seconds} seconds..."
                    )

                    time.sleep(
                        wait_seconds
                    )

                    continue

            raise error

    raise RuntimeError(
        "Gemini was temporarily unavailable "
        "after multiple attempts."
    ) from last_error