import time
import requests


OTHER_PERSON = {
    "Jill": "Nick",
    "Nick": "Jill"
}


def which_account() -> str:
    name = 0
    ACCOUNTS = ['House Avery', 'Jill and Nick']
    while name not in (1, 2):
        options = "\r\nSplitWiser Accounts:\r\n\t1. House Avery\r\n\t2. Jill and Nick"
        print(options)
        name = input("\r\nAlright, which SplitWiser list should we use? (1 or 2) ").strip()
        try:
            name = int(name)
            if name not in (1, 2):
                name = 0
                print("\r\nSorry, that didn't seem to be a 1 or 2. Please try again.\r\n")
                time.sleep(2)
        except:
            name = 0
            print("\r\nSorry, that didn't seem to be a 1 or 2. Please try again.\r\n")
            time.sleep(2)
    print(f"Nice. You've chosen account '{ACCOUNTS[name - 1]}'.")
    time.sleep(2)
    return ACCOUNTS[name - 1]


def handle_get_payload(url) -> dict:
    data = requests.get(url)
    if data.status_code == 200:
        return data.json()
    else:
        return {}

def terminal_pretty_print_spacer(line_str: str, max_tabs: int = 5) -> str:
    """ returns tabs! """
    t_string = ""
    line_len = len(line_str)
    lengths = [40, 32, 24, 16, 8]
    real_lengths = lengths[len(lengths)-max_tabs:]
    for length in real_lengths:
        if line_len < length:
            t_string += "\t"
    return t_string
