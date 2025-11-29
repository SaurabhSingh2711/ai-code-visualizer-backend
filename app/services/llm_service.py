# app/services/llm_service.py

import os
from openai import AzureOpenAI


class LLMService:
    """
    Azure OpenAI wrapper using YOUR .env variable names:
      - AZURE_OPENAI_KEY
      - AZURE_OPENAI_ENDPOINT
      - AZURE_OPENAI_DEPLOYMENT
      - AZURE_OPENAI_API_VERSION
    """

    def __init__(self):
        # Using your environment variables exactly as named
        self.api_key = os.getenv("AZURE_OPENAI_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

        if not self.api_key:
            raise ValueError("Missing env variable: AZURE_OPENAI_KEY")
        if not self.endpoint:
            raise ValueError("Missing env variable: AZURE_OPENAI_ENDPOINT")
        if not self.deployment:
            raise ValueError("Missing env variable: AZURE_OPENAI_DEPLOYMENT")

        # Create the Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version,
        )

    def ask(self, prompt: str) -> str:
        """
        Call Azure OpenAI Chat Completion using your configured deployment.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600
            )
            # FIX: Azure returns message.content (not a dict)
            return response.choices[0].message.content

        except Exception as e:
            return f"[AZURE LLM ERROR] {str(e)}"

