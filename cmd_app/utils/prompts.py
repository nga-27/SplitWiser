import time


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


def intro_and_choose_account(message: str) -> str:
    print(f"\r\n{message}\r\n")
    time.sleep(1)
    account = which_account()
    account_list = account.lower().split(' ')
    account_url = '_'.join(account_list)
    return account_url