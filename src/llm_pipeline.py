import json
import os
import time
from urllib import error, request

import yaml


CONFIG_PATH = "config/config.yaml"
MAX_RETRIES = 4
BACKOFF_SECONDS = 2


def _load_model_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    model_config = config.get("model", {})
    return {
        "llm_model": model_config.get("llm_model", "gemini-flash-latest"),
        "llm_provider": model_config.get("llm_provider", "gemini"),
        "project_name": model_config.get("project_name", ""),
        "project_number": model_config.get("project_number", ""),
    }


def generate_summary(prompt):
    """
    Send prompt to LLM and receive financial insights.
    """
    model_config = _load_model_config()
    provider = model_config["llm_provider"].lower()
    if provider != "gemini":
        raise ValueError(f"Unsupported llm_provider '{provider}'. Expected 'gemini'.")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Please set it in your environment.")

    model_name = model_config["llm_model"]
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model_name}:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}],
            }
        ]
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key,
    }
    resp_data = None
    for attempt in range(1, MAX_RETRIES + 1):
        req = request.Request(url, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=60) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
            break
        except error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="ignore")
            is_transient = exc.code == 503 and "UNAVAILABLE" in details.upper()
            if is_transient and attempt < MAX_RETRIES:
                time.sleep(BACKOFF_SECONDS * attempt)
                continue
            raise RuntimeError(
                f"Gemini API HTTP {exc.code}. Check key/project quota and permissions. Details: {details}"
            ) from exc
        except error.URLError as exc:
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF_SECONDS * attempt)
                continue
            raise RuntimeError(
                "Could not reach Gemini API. Check internet/proxy/firewall settings."
            ) from exc

    if resp_data is None:
        raise RuntimeError("Gemini API request failed after retries.")

    candidates = resp_data.get("candidates", [])
    if not candidates:
        raise RuntimeError(f"Gemini response did not include candidates: {resp_data}")

    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts:
        raise RuntimeError(f"Gemini response did not include content parts: {resp_data}")

    return parts[0].get("text", "")
