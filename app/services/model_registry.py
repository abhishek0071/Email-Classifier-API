"""
Maps friendly model names to Ollama model IDs and keeps a tiny “warm” cache.
"""
import time, requests
from functools import lru_cache
from ..core.settings import settings
from ..core.logger import logger

class ModelRegistry:
    def __init__(self, base_url: str, allowed: list[str]):
        self.base_url = base_url.rstrip("/")
        self.allowed  = set(allowed)

    def _generate(self, model: str, prompt: str, opts: dict):
        t0 = time.perf_counter()
        resp = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": opts,
            },
            timeout=120,
        )
        resp.raise_for_status()
        latency = (time.perf_counter() - t0) * 1000
        return resp.json()["response"], latency

    @lru_cache(maxsize=8)  # keeps model-name → True once first used
    def ensure_pulled(self, model: str):
        logger.info("First use of %s – pulling if necessary", model)
        requests.post(f"{self.base_url}/api/pull", json={"name": model}, timeout=None)

    def classify(
        self,
        *,
        model: str,
        subject: str,
        body: str,
        extra_options: dict | None = None,   # ← NEW
    ) -> tuple[str, float]:
        if model not in self.allowed and not model.endswith(".gguf-v2") and not model.endswith(".hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF"):
            raise ValueError(f"Model '{model}' is not allowed")
        self.ensure_pulled(model)

        prompt = (
            "You are an email security engine.\n"
            "Return ONLY one word: spam, authentic or phishing.\n\n"
            f"Subject: {subject}\n\n{body}"
        )
        # answer, latency = self._generate(model, prompt, {"num_predict": 16})
        # merge the caller-supplied opts with our defaults
        opts = {"num_predict": 16, **(extra_options or {})}
        answer, latency = self._generate(model, prompt, opts)
        label = answer.lower().split()[0]
        return label, latency

registry = ModelRegistry(settings.ollama_url, settings.allowed_models)
