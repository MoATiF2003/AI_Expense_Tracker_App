import asyncio

from app.ai.llm.groq_provider import (
    GroqProvider
)


async def main():

    provider = GroqProvider()

    response = await provider.generate(
        """
Return JSON:

{
    "message": "hello"
}
"""
    )

    print(response)


asyncio.run(main())