from typing import Union

from .constants import OTHER_PERSON

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


def format_transactions(transactions: dict, return_str: bool = False) -> Union[None, str]:
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
    
    if return_str:
        return full_string
    print(full_string)
    print("")
    return


def format_balances(summary: dict, return_str: bool = False) -> Union[None, str]:
    full_string = "-" * 85
    full_string = f"\r\n\r\n{full_string}"
    full_string += "\r\nPerson\t\tTotal\t\tHouse Avery\t\tJill and Nick\r\n\r\n"
    
    line_1 = f"Jill\t\t{summary['Total']['Jill']}\t\t"
    line_1 += f"{summary['House Avery']['Jill']}\t\t\t"
    line_1 += f"{summary['Jill and Nick']['Jill']}\r\n"

    line_2 = f"Nick\t\t{summary['Total']['Nick']}\t\t"
    line_2 += f"{summary['House Avery']['Nick']}\t\t\t"
    line_2 += f"{summary['Jill and Nick']['Nick']}\r\n"

    full_string += line_1
    full_string += line_2
    if return_str:
        return full_string
    print(full_string)
    print("")
    return
