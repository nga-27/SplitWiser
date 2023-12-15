from typing import Union

from .constants import OTHER_PERSON, PrintColor

DASH_LINE_LENGTH = 85

def terminal_pretty_print_spacer(line_str: str, max_tabs: int = 5, date: Union[None, str] = None) -> str:
    """ returns tabs! """
    lengths = [40, 32, 24, 16, 8]
    date_str = ""
    if date:
        date_str += f" ({date})"
        if len(line_str) + len(date_str) > lengths[0]:
            date_str = ""
    t_string = date_str
    line_len = len(line_str) + len(date_str)
    real_lengths = lengths[len(lengths)-max_tabs:]
    for length in real_lengths:
        if line_len < length:
            t_string += "\t"
    return t_string


def format_transactions(transactions: dict, table: str, return_str: bool = False,
                        color: Union[str, None] = None) -> Union[None, str]:
    if color is None:
        color = PrintColor.NORMAL
    table_name = ' '.join(table.upper().split('_'))
    full_string = f"****  {color}{table_name}{PrintColor.NORMAL}\r\n"
    full_string += "-" * DASH_LINE_LENGTH
    full_string = f"\r\n\r\n{full_string}"
    full_string += "\r\nID#: Trans Name\t\t\t\tAmount\t\tWho Paid\tOther Person Owes\r\n\r\n"
    for id, trans in transactions.items():
        t_string = f"{int(id)}: "
        t_string += f"'{trans['item']}'"
        t_string += terminal_pretty_print_spacer(t_string, date=trans['date'])

        amt = 0.0
        payer = ''
        for person, val in trans['paid_by_id'].items():
            # also equal-to because of payments that are worth 0
            if val >= amt:
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


def format_balances(summary: dict, return_str: bool = False) -> Union[None, str]:
    line_0 = f"****  {PrintColor.BLUE}BALANCES{PrintColor.NORMAL}\r\n"
    line_0 += "-" * DASH_LINE_LENGTH
    full_string = f"\r\n\r\n{line_0}"
    full_string += "\r\nPerson\t\tTotal\t\tHouse Avery\t\tJill and Nick\r\n\r\n"
    
    line_1 = f"{PrintColor.GREEN}Jill\t\t{summary['Total']['Jill']}\t\t"
    line_1 += f"{summary['House Avery']['Jill']}\t\t\t"
    line_1 += f"{summary['Jill and Nick']['Jill']}{PrintColor.NORMAL}\r\n"

    line_2 = f"{PrintColor.MAGENTA}Nick\t\t{summary['Total']['Nick']}\t\t"
    line_2 += f"{summary['House Avery']['Nick']}\t\t\t"
    line_2 += f"{summary['Jill and Nick']['Nick']}{PrintColor.NORMAL}\r\n"

    full_string += line_1
    full_string += line_2
    if return_str:
        return full_string
    print(full_string)
    print("")


def format_payments(payments_dict: dict, return_str: bool = False) -> Union[None, str]:
    line_0 = f"****  {PrintColor.HIGHLIGHT}PAYMENTS{PrintColor.NORMAL}\r\n"
    line_0 += "-" * DASH_LINE_LENGTH
    full_string = f"\r\n\r\n{line_0}"
    full_string += "\r\nID#: Date\t\tAmount\t\tWho Paid\tAccount\r\n\r\n"

    for _id, payment in payments_dict.items():
        t_string = f"{int(_id)}: "
        t_string += f"'{payment['date']}'"
        t_string += terminal_pretty_print_spacer(t_string, max_tabs=3)

        amt_str = f"${payment['amount']}"
        amt_str += terminal_pretty_print_spacer(amt_str, max_tabs=2)
        t_string += f"{amt_str}"
        t_string += f"{payment['payer']}\t\t"

        account = ' '.join([pay.capitalize() for pay in payment['account'].split('_')])
        t_string += f"{account}\r\n"
        full_string += t_string
    
    if return_str:
        return full_string
    print(full_string)
    print("")
