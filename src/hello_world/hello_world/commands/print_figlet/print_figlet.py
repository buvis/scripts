DEFAULT_FONT = 'doom'
DEFAULT_TEXT = 'World'

class CommandPrintFiglet:

    def __init__(self, cfg):
        res = cfg.get_key_value("font")

        if res.is_ok():
            self.font = res.payload
        else:
            self.font = DEFAULT_FONT

        res = cfg.get_key_value("text")

        if res.is_ok():
            self.text = res.payload
        else:
            self.text = DEFAULT_TEXT

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
