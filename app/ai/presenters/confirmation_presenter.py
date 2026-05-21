class ConfirmationPresenter:

    @classmethod
    def build_transaction_confirmation(
        cls,
        slots
    ):

        transaction_type = (
            slots.get(
                "transaction_type",
                "transaction"
            )
        )

        amount = slots.get(
            "amount"
        )

        account = slots.get(
            "account"
        )

        category = slots.get(
            "category",
            "Uncategorized"
        )

        return {

            "title":
                "Confirm Transaction",

            "message": (
                f"Confirm "
                f"{transaction_type} "
                f"of {amount} "
                f"from {account} "
                f"under {category}?"
            ),

            "transaction_preview": {

                "type":
                    transaction_type,

                "amount":
                    amount,

                "account":
                    account,

                "category":
                    category
            }
        }
