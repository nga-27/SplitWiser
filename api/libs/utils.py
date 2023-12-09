

def api_address_to_db_table(address_account: str) -> str:
    account_list = address_account.split('_')
    account_list = [word.capitalize() for word in account_list]
    try:
        index = account_list.index('And')
        account_list[index] = 'and'
    except:
        pass
    account = " ".join(account_list)
    return account
        