from rich.console import Console
from rich.prompt import Confirm

CHECKMARK = "[bold green1]\u2714[/bold green1]"
WARNING = "[bold orange3]\u26A0[/bold orange3]"
CROSSMARK = "[bold indian_red]\u2718[/bold indian_red]"
STYLE_SUCCESS_MSG = "spring_green1"
STYLE_WARNING_MSG = "light_goldenrod3"
STYLE_FAILURE_MSG = "bold light_salmon3"


class ConsoleAdapter:

    def __init__(self):
        self.console = Console(log_path=False)

    def format_success(self, message):
        return f" {CHECKMARK} [{STYLE_SUCCESS_MSG}]{message}[/{STYLE_SUCCESS_MSG}]"

    def success(self, message):
        self.console.print(self.format_success(message))

    def format_warning(self, message):
        return f" {WARNING} [{STYLE_WARNING_MSG}]{message}[/{STYLE_WARNING_MSG}]"

    def warning(self, message):
        self.console.print(self.format_warning(message))

    def format_failure(self, message, details=""):
        formatted_message = f" {CROSSMARK} [{STYLE_FAILURE_MSG}]{message}[/{STYLE_FAILURE_MSG}]"
        if details:
            formatted_message += " \n\n Details:\n\n {details}"

        return formatted_message

    def failure(self, message, details=""):
        self.console.print(self.format_failure(message, details))

    def panic(self, message, details=""):
        self.failure(message, details)
        exit()

    def status(self, message):
        return self.console.status(message, spinner="arrow3")

    def capture(self):
        return self.console.capture()

    def confirm(self, message):
        return Confirm.ask(message)

    def print(self, message):
        return self.console.print(message)

    def nl(self):
        return self.console.out("")


console = ConsoleAdapter()
