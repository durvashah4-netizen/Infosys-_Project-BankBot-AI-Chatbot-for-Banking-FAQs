class SessionStore:
    def __init__(self):
        self.sessions = {}

    def get_intent(self, session_id):
        return self.sessions.get(session_id, {}).get("intent")

    def set_intent(self, session_id, intent):
        self.sessions[session_id] = {"intent": intent}

    def reset(self, session_id):
        self.sessions[session_id] = {}
