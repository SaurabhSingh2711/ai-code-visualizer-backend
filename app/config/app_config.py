from openai import AsyncOpenAI
from .settings import get_settings
from ..utilities import logger


def get_llm_client():
    """
    Azure OpenAI ONLY (no OpenAI.com API key support).
    Requires the following settings in .env:
        AZURE_OPENAI_KEY=
        AZURE_OPENAI_ENDPOINT=
        AZURE_OPENAI_DEPLOYMENT_NAME=
    """

    settings = get_settings()

    if not (settings.AZURE_OPENAI_KEY and settings.AZURE_OPENAI_ENDPOINT and settings.AZURE_OPENAI_DEPLOYMENT_NAME):
        logger.error("Azure OpenAI configuration missing. Check your .env file.")
        raise ValueError(
            "Azure OpenAI configuration missing. "
            "Please add AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_DEPLOYMENT_NAME."
        )

    logger.info("Initializing Azure OpenAI client...")

    client = AsyncOpenAI(
        api_key=settings.AZURE_OPENAI_KEY,
        base_url=f"{settings.AZURE_OPENAI_ENDPOINT}/openai/deployments/{settings.AZURE_OPENAI_DEPLOYMENT_NAME}",
        api_version="2024-02-01",
    )

    return client
