class CommandPrintFiglet:
    def __init__(self: "CommandPrintFiglet", font: str, text: str) -> None:
        self.font = font
        self.text = text

    def execute(self: "CommandPrintFiglet") -> None:
        try:
            from pyfiglet import Figlet

            f = Figlet(font=self.font)
        except ImportError:
            f = None

        print("\n")

        if f is None:
            print(f"Hello {self.text}!\n\n")
        else:
            print(f.renderText(f"Hello {self.text}!"))
