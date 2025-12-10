''''python
# filepath: d:\Documents\Visual Studio Code\WeThinkCode Hackathon\Tech Titans MVP\llama_client.py
import os
import requests
from typing import Optional

# Optional local import (llama-cpp-python)
try:
    from llama_cpp import Llama  # type: ignore
except Exception:
    Llama = None  # local model not available

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "remote").lower()
LLM_API_URL = os.environ.get("LLM_API_URL", "").strip()
LLM_API_KEY = os.environ.get("LLM_API_KEY", "").strip()
LOCAL_LLAMA_MODEL_PATH = os.environ.get("LOCAL_LLAMA_MODEL_PATH", "").strip()

def _call_remote(prompt: str, model: Optional[str] = None, timeout: int = 15) -> str:
    if not LLM_API_URL:
        raise RuntimeError("LLM_API_URL not set for remote LLM_PROVIDER")
    headers = {}
    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"
    payload = {
        "prompt": prompt,
        "model": model or "default",
        "max_tokens": 512
    }
    resp = requests.post(LLM_API_URL, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    # try common keys returned by Llama-style APIs
    for key in ("text", "output", "choices"):
        if key in data:
            if key == "choices" and isinstance(data[key], list) and data[key]:
                c = data[key][0]
                return c.get("text") or c.get("message") or str(c)
            return data[key]
    # fallback to full JSON
    return str(data)

def _call_local(prompt: str, model: Optional[str] = None) -> str:
    if Llama is None:
        raise RuntimeError("llama-cpp-python not installed or reachable")
    path = model or LOCAL_LLAMA_MODEL_PATH
    if not path:
        raise RuntimeError("LOCAL_LLAMA_MODEL_PATH not set for local model")
    client = Llama(model_path=path)
    out = client(prompt, max_tokens=512)
    # llama-cpp returns dict with 'choices' etc.
    if isinstance(out, dict):
        choices = out.get("choices")
        if choices and isinstance(choices, list):
            txt = choices[0].get("text") or choices[0].get("message")
            return txt or str(out)
    return str(out)

def generate(prompt: str, model: Optional[str] = None) -> str:
    if LLM_PROVIDER == "local":
        return _call_local(prompt, model)
    return _call_remote(prompt, model)