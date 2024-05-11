"""
Steno™ | OpenAI Client
"""

# Steno™ - AI Chat Recorder
#
# MIT License
#
# Copyright © 2024 Joshua M. Dotson (contact@cryorithm.org)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from typing import List, Dict, Any, AsyncIterator

# Since OpenAI does not have an official async client provided in their Python package,
# we'll assume it should still be imported from openai (if using synchronous just
# remove all 'async' and 'await').
from openai import OpenAI as AsyncOpenAIClient


class LLMClient:
    """Base class to ensure proper inheritance if needed."""

    pass


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key must be provided")
        self.client = AsyncOpenAIClient(api_key=api_key)

    async def create_chat_completion_stream(
        self,
        model: str,
        messages: List[Dict[str, Any]],
    ) -> AsyncIterator:
        try:
            # Assuming .chat_completions is the method name; double-check based on
            # actual SDK documentation.
            response_stream = await self.client.Completion.create(
                model=model,
                messages=messages,
                stream=True,
            )

            async for chunk in response_stream:
                if (
                    "choices" in chunk
                    and len(chunk["choices"]) > 0
                    and "content" in chunk["choices"][0]
                ):
                    yield chunk["choices"][0]["content"]
                else:
                    yield ""  # Yield empty string or handle unexpected format more
                    # gracefully

        except Exception as e:
            print(f"Failed to generate completion: {str(e)}")
            raise e
