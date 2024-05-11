from abc import ABC, abstractmethod
from typing import AsyncIterator, List, Dict, Any


class LLMClient(ABC):
    @abstractmethod
    async def create_chat_completion_stream(
        self,
        model: str,
        messages: List[Dict[str, Any]],
    ) -> AsyncIterator:
        pass
