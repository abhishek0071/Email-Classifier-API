"""
Light wrapper that picks Ollama options based on model format.
"""
from ..core.constants import FORMAT_OPTIONS
from ..core.logger import logger

def detect_format(model_name: str) -> str:
    if model_name.endswith(".gguf-v2") or model_name.startswith("gguf-v2/"):
        return "gguf-v2"
    if model_name.endswith(".gguf") or model_name.startswith("gguf-v1/"):
        return "gguf-v1"
    return "other"

def options_for(model_name: str) -> dict:
    fmt = detect_format(model_name)
    opts = FORMAT_OPTIONS.get(fmt, {})
    logger.debug("Model %s detected as %s, opts=%s", model_name, fmt, opts)
    return opts
