import json
import logging
import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest").strip()

    def is_available(self) -> bool:
        available = bool(self.api_key)
        if not available:
            logger.warning("Gemini API key not found; falling back to heuristic scoring.")
        return available

    def generate_json(self, prompt: str) -> Optional[Dict[str, Any]]:
        if not self.is_available():
            return None

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt}
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json",
            },
        }

        try:
            logger.info("Calling Gemini model '%s'.", self.model)
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            if not text:
                logger.warning("Gemini returned empty text payload.")
                return None
            logger.info("Gemini raw response text (truncated): %s", text[:300])
            return json.loads(text)
        except requests.HTTPError:
            status_code = response.status_code if "response" in locals() else "unknown"
            body_preview = ""
            try:
                body_preview = response.text[:300]
            except Exception:
                body_preview = ""
            logger.error("Gemini request failed with status %s. Body: %s", status_code, body_preview)
            return None
        except requests.RequestException as exc:
            logger.error("Gemini request failed: %s", type(exc).__name__)
            return None
        except (json.JSONDecodeError, KeyError, IndexError) as exc:
            logger.exception("Gemini response parse failed: %s", exc)
            return None
