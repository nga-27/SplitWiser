""" Constants for the application + colors for command line printing fun """
from colorama import Fore, Back

OTHER_PERSON = {
    "Jill": "Nick",
    "Nick": "Jill"
}

AVAILABLE_PEOPLE = ('Jill', 'Nick')

ACCOUNTS = ('House Avery', 'Jill and Nick', 'Archived - House Avery', 'Archived - Jill and Nick')

# UI-Specific constants
class PrintColor: # pylint: disable=too-few-public-methods
    """ Color mapping from colorama """
    BLACK = Fore.BLACK
    WHITE = Fore.WHITE
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    CYAN = Fore.CYAN
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    NORMAL = f"{Fore.RESET}{Back.RESET}"
    HIGHLIGHT = Back.LIGHTBLUE_EX
