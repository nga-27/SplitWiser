from .utils import handle_get_payload, format_transactions, intro_and_choose_account


def view_handler(base_url: str) -> bool:
    account = intro_and_choose_account("Sweet, let's check out the transactions that exist.")
    transactions = handle_get_payload(f"{base_url}/transactions/{account}")
    str_transactions = format_transactions(transactions)
    print(str_transactions)
    return True
