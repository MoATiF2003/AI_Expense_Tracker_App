class ConversationStateManager:

    _pending_workflows = {}

    @classmethod
    def save_workflow(cls, session_id, workflow_data):
        cls._pending_workflows[session_id] = workflow_data

    @classmethod
    def get_workflow(cls, session_id):
        return cls._pending_workflows.get(session_id)
    
    @classmethod
    def clear_workflow(cls, session_id):
        if session_id in cls._pending_workflows:
            del cls._pending_workflows[session_id]