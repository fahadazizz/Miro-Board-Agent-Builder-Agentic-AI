import os
from typing import Optional

class Config:
    # Hardcoded for now as per user request, but ideally should be env var
    MIRO_ACCESS_TOKEN: Optional[str] = os.getenv("MIRO_ACCESS_TOKEN", "eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_Z9hj-1iSRDmhGWgMcRGyyXlBXYA")
    
    # Ollama settings
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3-coder:480b-cloud") # Updated to a known good model
    
    TEST_BOARD_ID: Optional[str] = os.getenv("TEST_BOARD_ID")

    # LangSmith Tracing
    LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "true")
    LANGCHAIN_ENDPOINT: str = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "miro-agent-builder")

    @staticmethod
    def validate():
        if not Config.MIRO_ACCESS_TOKEN:
            print("Warning: MIRO_ACCESS_TOKEN is not set. API calls will fail.")
