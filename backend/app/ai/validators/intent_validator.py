class IntentValidator:

    VALID_INTENTS = [
        "create_transaction",
        "get_transactions",
        "create_account",
        "create_category"
    ]

    @classmethod
    def validate(cls, intent: str) -> bool:
        return (
            intent in cls.VALID_INTENTS
        )