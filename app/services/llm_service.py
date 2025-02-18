# app/services/llm_service.py
import aiohttp
from app.core.config import settings

class LLMService:
    @staticmethod
    async def generate_summary(content: str) -> str:
        prompt = f"Please provide a concise summary of the following text:\n\n{content}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.OLLAMA_API_URL}/api/generate",
                json={
                    "model": settings.MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                }
            ) as response:
                result = await response.json()
                return result.get("response", "")

    @staticmethod
    async def answer_question(content: str, question: str) -> str:
        prompt = f"Based on the following content:\n\n{content}\n\nPlease answer this question: {question}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.OLLAMA_API_URL}/api/generate",
                json={
                    "model": settings.MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                }
            ) as response:
                result = await response.json()
                return result.get("response", "")
