from openai import OpenAI
import os
import json

class BusinessAgent:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_summary(self, categories):
        prompt = f"""
        Create a business-friendly email summary
        explaining this system error distribution:
 
        {json.dumps(categories)}

        Explain impact in simple language.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content