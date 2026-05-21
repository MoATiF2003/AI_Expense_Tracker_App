import json
from app.core.config import settings

from groq import Groq

from app.ai.llm.base_llm import BaseLLM

class GroqProvider(BaseLLM):
    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )
    
    async def generate(self, prompt: str):
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            response_format={
                "type": "json_object"
            }
        )

        content = completion.choices[0].message.content

        return json.loads(content)