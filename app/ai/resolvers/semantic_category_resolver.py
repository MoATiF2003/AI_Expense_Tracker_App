class SemanticCategoryResolver:

    def __init__(self, llm_provider):
        self.llm_provider = llm_provider

    async def resolve_category(self, user_message: str, existing_categories: list[str]):
        prompt = f"""
You are a finance category resolution system.

Existing Categories:
{existing_categories}

User Message:
{user_message}

Rules:
1. Prefer matching existing categories if semantically appropriate.
2. ONLY propose a new category if no existing category fits well.
3. Return ONLY valid JSON.
4. Do not explain anything.
5. Do not use markdown.

JSON Format:
{{
    "matched_category": "string or null",
    "proposed_new_category": "string or null"
}}

Example 1:
{{
    "matched_category": "Entertainment",
    "proposed_new_category": null
}}

Example 2:
{{
    "matched_category": null,
    "proposed_new_category": "Subscription"
}}
"""
        response = await self.llm_provider.generate(prompt)

        return response