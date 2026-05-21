class ClarificationGenerator:
    QUESTIONS = {
        "amount": "How much was the transaction?",
        "account": "Which account did you use?",
        "transaction_type": "Was this expense, income or transfer?"
    }

    @classmethod
    def generate_question(cls, missing_fields):
        first_missing_field = missing_fields[0]

        return cls.QUESTIONS.get(first_missing_field, f"Please provide - {first_missing_field}")