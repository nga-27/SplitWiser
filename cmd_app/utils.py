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

def handle_delete_id(url) -> bool:
    response = requests.delete(url)
    return response.status_code == 201

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

def format_transactions(transactions: dict) -> str:
    full_string = "-" * 85
    full_string = f"\r\n\r\n{full_string}"
    full_string += "\r\nID#: Trans Name\t\t\t\tAmount\t\tWho Paid\tOther Person Owes\r\n\r\n"
    for id, trans in transactions.items():
        t_string = f"{int(id)}: "
        t_string += f"'{trans['item']}'"
        t_string += terminal_pretty_print_spacer(t_string)

        amt = 0.0
        payer = ''
        for person, val in trans['paid_by_id'].items():
            if val > amt:
                amt = val
                payer = person

        amt_str = f"${amt}"
        amt_str += terminal_pretty_print_spacer(amt_str, max_tabs=2)
        t_string += f"{amt_str}"
        t_string += f"{payer}\t\t"
        t_string += f"${trans['owed_by_id'][OTHER_PERSON[payer]]}\r\n"
        full_string += t_string
    return full_string
