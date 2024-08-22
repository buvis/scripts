DEFAULT_FONT = "doom"
DEFAULT_TEXT = "World"


class CommandPrintFiglet:
    def __init__(self, cfg):
        res = cfg.get_configuration_item("font", DEFAULT_FONT)
        self.font = res.payload if res.is_ok() else DEFAULT_FONT

        res = cfg.get_configuration_item("text", DEFAULT_TEXT)
        self.text = res.payload if res.is_ok() else DEFAULT_TEXT

    def execute(self):
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
