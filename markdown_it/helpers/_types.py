class ParseResult:
    __slots__ = ("lines", "ok", "pos", "str")

    def __init__(self) -> None:
        self.ok = False
        self.pos = 0
        self.lines = 0
        self.str = ""
