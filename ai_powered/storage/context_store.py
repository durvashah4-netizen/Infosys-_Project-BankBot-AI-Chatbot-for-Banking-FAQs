class ContextStore:
    def __init__(self):
        self.context = {}

    def update(self, key, value):
        self.context[key] = value

    def reset(self):
        self.context = {}
