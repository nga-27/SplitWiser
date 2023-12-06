import time

from .utils import which_account, handle_get_payload, OTHER_PERSON, terminal_pretty_print_spacer


def intro_and_choose_account() -> str:
    print("\r\nSweet, let's check out the transactions that exist.\r\n")
    time.sleep(1)
    account = which_account()
    account_list = account.lower().split(' ')
    account_url = '_'.join(account_list)
    return account_url

def format_transactions(transactions: dict) -> str:
    full_string = "-" * 45
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


##########################################

def view_handler(base_url: str) -> bool:
    account = intro_and_choose_account()
    transactions = handle_get_payload(f"{base_url}/transactions/{account}")
    str_transactions = format_transactions(transactions)
    print(str_transactions)
    return True