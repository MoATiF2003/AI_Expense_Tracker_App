class ClarificationValidator:

    @classmethod
    def validate_account(cls, account):
        if not isinstance(account, str):
            return False
        
        if len(account.strip()) == 0:
            return False
        
        return True
    

    