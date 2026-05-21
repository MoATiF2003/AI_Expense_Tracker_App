VALID_INTENTS = [
    "create_transaction",
    "unknown"
]

def build_intent_prompt(message: str):
    return f"""
You are an AI intent classifier.

Your task:
Identify the user's intent.

Allowed intents:
{VALID_INTENTS}

Rules:
- Return ONLY valid JSON
- Do NOT explain
- Do NOT add markdown
- Do NOT add extra text
- If uncertain, return "unknown"

User message:
"{message}"

Return JSON in EXACT format:

{{
    "intent": "create_transaction"
}}
"""