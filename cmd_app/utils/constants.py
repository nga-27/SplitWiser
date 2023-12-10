# At some point, I *might* convert this to environment variables or the like
from colorama import Fore

OTHER_PERSON = {
    "Jill": "Nick",
    "Nick": "Jill"
}

AVAILABLE_PEOPLE = ('Jill', 'Nick')

# UI-Specific constants
class PrintColor:
    BLACK = Fore.BLACK
    WHITE = Fore.WHITE
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    CYAN = Fore.CYAN
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    NORMAL = Fore.RESET
