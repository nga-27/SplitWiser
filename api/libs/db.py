from typing import List
import datetime

import pandas as pd

from api.models.models import Transaction, AddTransaction
from api import main


# Internal for INIT!
def handle_loading_summary_sheet(raw_df: pd.DataFrame) -> dict:
    sub_dict = {key: {} for key in raw_df.keys()}
    sub_dict.pop('Person')
    for key in sub_dict:
        for item, value in raw_df[key].items():
            sub_dict[key][raw_df['Person'][item]] = value
    return sub_dict


def load_people_involved(raw_df: pd.DataFrame) -> dict:
    sub_dict = {
        person_id: {"id": person_id, "name": person_name} \
            for person_id, person_name in raw_df['Summary']['Person'].items()
    }
    # Reverse the operation (search via name)
    for person_id, person_name in raw_df['Summary']['Person'].items():
        sub_dict[person_name] = {"id": person_id, "name": person_name}
    list_of_people = []
    for person_id in sub_dict:
        try:
            int(person_id)
            continue
        except:
            list_of_people.append(person_id)
    sub_dict['__list__'] = list_of_people
    return sub_dict

def money_by_involved_handler(transaction_dict: dict, index: int, key: str, _db: dict) -> List[dict]:
    money_list = []
    if key not in ('Owes', 'Paid'):
        return money_list
    for person_id, person_obj in _db['People'].items():
        try:
            int(person_id)
            val = transaction_dict[f"{person_obj['name']} {key}"][index]
            money_list.append({person_obj['name']: val})
        except:
            continue
    return money_list


def handle_transaction_sheets(raw_df: pd.DataFrame, sheet_name: str, _db: dict) -> dict:
    trans_dict = {}
    raw_df.dropna(inplace=True)
    df_as_dict = raw_df.to_dict()
    for i in range(len(df_as_dict['Date'])):
        transaction = Transaction(
            id=str(i),
            date=df_as_dict['Date'][i].strftime("%m/%d/%Y"),
            item=df_as_dict['Transaction Item'][i],
            paid_by_id=money_by_involved_handler(df_as_dict, i, 'Paid', _db),
            owed_by_id=money_by_involved_handler(df_as_dict, i, 'Owes', _db)
        )
        trans_dict[str(i)] = transaction.dict()
    return trans_dict


# Public-facing init_db structure for managing functionality
def init_db(xlsx_path: str) -> dict:
    df_db = pd.read_excel(xlsx_path, sheet_name=None)
    modded_db = {key: {} for key in df_db.keys()}
    # People (internal key) first
    modded_db['People'] = load_people_involved(df_db)
    modded_db['Summary'] = handle_loading_summary_sheet(df_db['Summary'])
    for key in df_db:
        if key not in ('Summary', 'People'):
            modded_db[key] = handle_transaction_sheets(df_db[key], key, modded_db)
    return modded_db

##########################################################

def get_all_transactions(ledger_sheet: str) -> dict:
    return main.DB[ledger_sheet]


def add_transaction(add_transaction: AddTransaction, ledger_sheet: str):
    num_records = len(main.DB[ledger_sheet])
    people = main.DB['People']['__list__']
    paid = [{add_transaction.paid_by_name: add_transaction.paid_amount}]
    for person in people:
        if person not in [item.keys() for item in paid]:
            paid.append({person: 0})
    owes = [{add_transaction.paid_by_name: 0}]
    for person in people:
        if person not in [item.keys() for item in owes]:
            owes.append({person: add_transaction.other_person_owes})

    record = Transaction(
        date=datetime.datetime.now().strftime("%m/%d/%Y"),
        id=str(num_records),
        item=add_transaction.item,
        paid_by_id=paid,
        owed_by_id=owes
    ).dict()
    main.DB[ledger_sheet][record["id"]] = record
    return main.DB
