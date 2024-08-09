class AdapterResponse:

    def __init__(self, code=0, payload=""):
        self.code = code
        self.payload = payload

    def is_ok(self):
        return self.code == 0

    def is_nok(self):
        return self.code != 0

    def __repr__(self):
        return f"{self.payload} ({self.code})"
