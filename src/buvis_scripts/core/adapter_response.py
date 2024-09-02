class AdapterResponse:
    code: int
    payload: object

    def __init__(
        self: "AdapterResponse",
        code: int = 0,
        payload: object = None,
    ) -> None:
        self.code = code
        self.payload = payload

    def is_ok(self: "AdapterResponse") -> bool:
        return self.code == 0

    def is_nok(self: "AdapterResponse") -> bool:
        return self.code != 0

    def __repr__(self: "AdapterResponse") -> str:
        return f"{self.payload} ({self.code})"
