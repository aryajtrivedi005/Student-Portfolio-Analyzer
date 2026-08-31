import requests
import json
import logging
import os
import streamlit as st
from typing import Dict, Any, List, Optional

def get_ollama_base_url() -> str:
    """Retrieve Ollama base URL from Streamlit secrets, env vars, or default localhost."""
    url = None
    try:
        if hasattr(st, "secrets") and "OLLAMA_BASE_URL" in st.secrets:
            url = st.secrets["OLLAMA_BASE_URL"]
    except Exception:
        pass

    if not url:
        url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    return url.rstrip('/')

class OllamaClient:
    def __init__(self):
        self.headers = {
            "ngrok-skip-browser-warning": "true",
            "User-Agent": "Student360AI/1.0"
        }

    @property
    def host(self) -> str:
        return get_ollama_base_url()

    def is_available(self) -> bool:
        """Check if local or tunneled Ollama server is running."""
        try:
            res = requests.get(f"{self.host}/api/tags", headers=self.headers, timeout=3.0)
            return res.status_code == 200
        except Exception as e:
            logging.warning(f"Ollama availability check failed at {self.host}: {e}")
            return False

    def list_models(self) -> List[str]:
        """Fetch list of installed Ollama models."""
        try:
            res = requests.get(f"{self.host}/api/tags", headers=self.headers, timeout=4.0)
            if res.status_code == 200:
                data = res.json()
                models = [m['name'] for m in data.get('models', [])]
                return models
        except Exception as e:
            logging.warning(f"Failed to fetch Ollama models from {self.host}: {e}")
        return []

    def select_best_model(self) -> Optional[str]:
        """Automatically select the best available model (prefers Llama 3.x)."""
        models = self.list_models()
        if not models:
            return None

        for m in models:
            if "llama3" in m.lower():
                return m
        for m in models:
            if "mistral" in m.lower() or "gemma" in m.lower() or "phi" in m.lower():
                return m
        return models[0]

    def generate(self, prompt: str, system_prompt: str = "", model: Optional[str] = None, timeout: int = 30) -> Optional[str]:
        """Send prompt to Ollama and return text response."""
        if not self.is_available():
            return None

        selected_model = model or self.select_best_model()
        if not selected_model:
            return None

        payload = {
            "model": selected_model,
            "prompt": prompt,
            "system": system_prompt or "You are Student360 AI, an expert career readiness advisor for university students.",
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        }

        try:
            res = requests.post(f"{self.host}/api/generate", headers=self.headers, json=payload, timeout=timeout)
            if res.status_code == 200:
                data = res.json()
                return data.get('response', '').strip()
        except Exception as e:
            logging.warning(f"Ollama generation failed or timed out at {self.host}: {e}")

        return None

# Singleton client instance
ollama_client = OllamaClient()
