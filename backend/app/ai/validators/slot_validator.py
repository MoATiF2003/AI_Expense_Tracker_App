class SlotValidator:

    VALID_TRANSACTION_TYPES = [
        "income",
        "expense",
        "transfer"
    ]

    @classmethod
    def validate_transaction_slots(cls, slots: dict):
        required_field = [
            "amount",
            "category",
            "account",
            "transaction_type"
        ]

        missing_fields = []

        for field in required_field:
            if field not in slots or slots[field] is None:
                missing_fields.append(field)

        if missing_fields:
            return {
                "valid": False,
                "error": (
                    "Missing required fields"
                ),
                "missing_fields": missing_fields
            }
        
        try:
            amount = float(slots["amount"])
            if amount <= 0:
                return {
                    "valid": False,
                    "error": (
                        "Amount must be greater than 0"
                    )
                }
        
        except Exception:
            return {
                "valid": False,
                "error": (
                    "Invalid amount format"
                )       
            }
        
        if slots["transaction_type"] not in cls.VALID_TRANSACTION_TYPES:
            return {
                "valid": False,
                "error": (
                    "Invalid transaction type"
                )             
            }
        return {
            "valid": True
        }