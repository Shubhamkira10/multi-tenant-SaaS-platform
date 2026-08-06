from __future__ import annotations

import json
from google import genai
import time

from app.core.config import settings


class GeminiClient:

    def __init__(self):

        api_key = settings.GEMINI_API_KEY

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        self.model = "gemini-2.5-flash"


    def generate(self, prompt: str):

        for _ in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                text = (
                    response.text
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

                return json.loads(text)

            except Exception:
                time.sleep(2)

        raise RuntimeError("Gemini unavailable after 3 retries.")