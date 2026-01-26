import httpx
import logging
from typing import List, Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)

async def chat_completion(
    messages: List[Dict[str, str]],
    model: str | None = None,
    max_tokens: int = 1000,
    temperature: float = 0.7,
) -> str:
    """
    Send conversation to LM studio, return assistant reply
    """
    model = model or settings.lm_studio_model
    
    payload = {
        "model": model or "*",  # ← "*" works for any loaded model
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,  # ← explicit
    }
    
    logger.info(f"Sending to LM Studio: {len(messages)} messages")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        url = str(settings.lmstudio_base_url).rstrip("/") + "/v1/chat/completions"
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"LM Studio response keys: {list(data.keys())}")
        
        if "choices" not in data or not data["choices"]:
            logger.error(f"Empty choices: {data}")
            raise ValueError(f"LM Studio empty response: {data.get('error', data)}")
        
        choice = data["choices"][0]
        if "message" not in choice or "content" not in choice["message"]:
            logger.error(f"Bad choice format: {choice}")
            raise ValueError(f"Bad response format: {choice}")
            
        return choice["message"]["content"]
