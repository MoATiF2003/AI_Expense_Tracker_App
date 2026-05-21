def build_slot_prompt(message: str):
    return f"""
You are an AI financial transaction parser.

Extract transaction information
from the user message.

Rules:
- Return ONLY valid JSON
- Do NOT explain
- Do NOT add markdown
- Missing fields should be null

Extract:
- amount
- account
- transaction_type
- description

User message:
"{message}"

Return JSON in EXACT format:

{{
    "amount": 250,
    "account": "Fed Account",
    "transaction_type": "expense",
    "description": "Netflix Subscription"
}}
"""