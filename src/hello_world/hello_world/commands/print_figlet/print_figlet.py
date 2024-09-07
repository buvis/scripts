from buvis.pybase.configuration import ConfigurationKeyNotFoundError

DEFAULT_FONT = "doom"
DEFAULT_TEXT = "World"


class CommandPrintFiglet:
    def __init__(self, cfg):
        try:
            self.font = cfg.get_configuration_item("font", DEFAULT_FONT)
        except ConfigurationKeyNotFoundError as _:
            self.font = DEFAULT_FONT

        try:
            self.text = cfg.get_configuration_item("text", DEFAULT_TEXT)
        except ConfigurationKeyNotFoundError as _:
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
