from openai import OpenAI
import os
import json
import httpx


class LLMAgent:

    def __init__(self):
        apikey = os.getenv("OPENAI_API_KEY")

        proxy_url = "http://proxyo.fnb.co.za:8080"

        http_client = httpx.Client(
            proxy=proxy_url,
            verify=False  # often needed behind corporate SSL inspection
        )

        self.client = OpenAI(
            api_key=apikey,
            http_client=http_client
        )

    def classify(self, message: str) -> str:

        prompt = f"""
You are a senior production support engineer analyzing application errors.

Your task is to review the error logs provided and determine the most appropriate category for each error based on its root cause.

Categories:
1. Database Errors related to SQL, database connectivity, query failures, deadlocks, timeouts.
2. API Errors related to REST/HTTP calls or external services.
3. Authentication Errors related to login, tokens, OAuth, JWT validation.
4. Infrastructure Errors related to filesystem, network, server, disk, environment configuration.
5. Unknown If root cause cannot be determined.

Input Errors:
{message}

Return JSON like:

[
  {{
    "error": "<original error message>",
    "category": "Database",
    "reason": "SQL timeout occurred"
  }}
]
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
)
        

        return response.choices[0].message.content.strip()