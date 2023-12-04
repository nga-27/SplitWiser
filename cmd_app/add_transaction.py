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
        name = input("\r\nAlright, which SplitWiser list should this go to? (1 or 2) ").strip()
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
            

def get_valid_name(message: str) -> str:
    print("")
    name2 = "N"
    while 'N' in name2:
        name = input(f"{message} ")
        name2 = input(f"Nice. Cool with '{name}'? (just hit enter if yes, or 'N' if to redo it.)").upper()
    return name

def get_valid_amount(message: str) -> float:
    amt = -1.0
    while amt < 0.0:
        print("")
        ew_input = input(f"{message} ")
        if '$' in ew_input:
            ew_input = ew_input.split('$')[-1]
            ew_input = ew_input.strip()
        try:
            amt = float(ew_input)
            if amt < 0.0:
                print("I'm sorry, but a payment must be $0 or more.")
                time.sleep(2)
                continue
        except ValueError:
            amt = -1.0
            print("I'm sorry, that didn't seem to be a valid amount. Try in the form of XXX.YY or XXX.")
            time.sleep(2)
            continue

        verify = input(f"Are you happy with the amount of ${amt}? (enter for yes) ")
        if verify != '':
            amt = -1.0
    return amt

def who_paid() -> str:
    print("")
    okay_for_transaction = False
    while not okay_for_transaction:
        person = ""
        while person not in ('Jill', 'Nick'):
            person = input("Who paid for this transaction? (Jill or Nick) ")
            if 'jill' not in person.lower() and 'nick' not in person.lower():
                print("Hmmm. That didn't look like 'Jill' or 'Nick'. Please try again.\r\n")
                person = ""
                time.sleep(2)
                continue
            if 'jill' in person.lower():
                person = 'Jill'
            else:
                person = 'Nick'
        
        is_fine = input(f"Cool. Are you good with '{person}' paying for this? (hit enter if yes) ")
        if is_fine == '':
            okay_for_transaction = True

    return person

def how_to_split_transaction(amt: float, who_paid: str) -> float:
    """ returns what the other person pays """
    OPTION_SPLITS = ["50% / 50%", "100% the other person", f"100% {who_paid}", "60% Nick, 40% Jill"]
    OPTION_MATH = [0.5, 1.0, 0.0, 0.4]
    if who_paid == 'Jill':
        OPTION_MATH[3] = 0.6

    valid_split = False
    while not valid_split:
        print("\r\nHow would you like to split the transaction? ")
        options = "Options include:\r\n\r\n"
        options += "\t1. 50%/50%\r\n"
        options += "\t2. 100% the other person owes\r\n"
        options += f"\t3. 100% {who_paid}, so nothing is owed\r\n"
        options += "\t4. 60% Nick, 40% Jill\r\n\r\n"
        print(options)
        split_option = input("Enter the number (1-4) for the option you want: ")
        try:
            split_option = int(split_option.strip())
            valid_split = True
        except:
            print(f"\r\nSorry, the provided '{split_option}' didn't seem to be numeric 1-4. Please try again.")
            time.sleep(2)

    print(f"Split option is: {OPTION_SPLITS[split_option - 1]}\r\n")
    return round(OPTION_MATH[split_option - 1] * amt, 2)

    
#############################################

def add_handler(base_url: str) -> bool:
    print("\r\nCool, let's **ADD** a transaction. We'll start by asking some questions about it...")
    time.sleep(2)

    transaction_name = get_valid_name("First, what name should we give this transaction?")
    account = which_account()
    person = who_paid()
    person_paid = get_valid_amount(f"Cool. How much did {person} pay?")
    other_person = how_to_split_transaction(person_paid, person)

    time.sleep(1)
    message = "Summary of transaction:\r\n\r\n"
    message += f"\tAccount: {account}\r\n"
    message += f"\tNamed: '{transaction_name}'\r\n"
    message += f"\t{person} paid ${person_paid}\r\n"
    message += f"\t{OTHER_PERSON[person]} now OWES ${other_person}"
    print(message)
    time.sleep(4)
    print("\r\n\r\n")

    transaction = {
        "item": transaction_name,
        "paid_by_name": person,
        "paid_amount": person_paid,
        "other_person_owes": other_person
    }
    db_table_name_list = account.lower().split(' ')
    db_table_name = '_'.join(db_table_name_list)
    requests.post(f"{base_url}/transactions/{db_table_name}", json=transaction)
        
    return True