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


def input_id_handler(id_str: str, num_transactions: int) -> str:
    id_str = id_str.strip()
    if 'menu' in id_str.lower():
        return 'menu'
    try:
        id_ = int(id_str)
        if id_ > num_transactions - 1 or id_ < 0:
            print(f"'{id_}' is not in range of 0 - {num_transactions - 1}. Please try again.\r\n")
            time.sleep(1)
            return ""
    except:
        print(f"'{id_}' is not a valid number in range of 0 - {num_transactions - 1}. Please try again.\r\n")
        time.sleep(1)
        return ""
    return str(id_)


def who_paid(is_settle_up_payment: bool = False) -> str:
    print("")
    okay_for_transaction = False
    first_input = 'made this payment' if is_settle_up_payment else 'paid for this transaction'
    second_input = 'making this payment' if is_settle_up_payment else 'paying for this'
    while not okay_for_transaction:
        person = ""
        while person not in ('Jill', 'Nick'):
            person = input(f"Who paid {first_input}? (Jill or Nick) ")
            if 'jill' not in person.lower() and 'nick' not in person.lower():
                print("Hmmm. That didn't look like 'Jill' or 'Nick'. Please try again.\r\n")
                person = ""
                time.sleep(2)
                continue
            if 'jill' in person.lower():
                person = 'Jill'
            else:
                person = 'Nick'
        
        is_fine = input(f"Cool. Are you good with '{person}' {second_input}? (hit enter if yes) ")
        if is_fine == '':
            okay_for_transaction = True

    return person
