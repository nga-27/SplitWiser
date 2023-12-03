import os
from typing import List, Dict
import datetime
import json

import pandas as pd

from api.models.models import Transaction

DB_DIR = "__internal__"
DB_PATH = os.path.join(DB_DIR, "db.json")


###########################################
def reset_db():
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
    with open(DB_PATH, 'w') as db_file:
        # wipe the old temp db clean!
        json.dump({}, db_file)
    return

def update_db(db_obj: dict):
    with open(DB_PATH, 'w') as dbf:
        json.dump(db_obj, dbf)
    return

def read_db():
    db_obj = {}
    with open(DB_PATH, 'r') as dbf:
        db_obj = json.load(dbf)
    return db_obj

###########################################

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

def money_by_involved_handler(transaction_dict: dict, index: int, key: str, _db: dict) -> Dict[str, float]:
    money_dict = {}
    if key not in ('Owes', 'Paid'):
        return money_dict
    for person_id, person_obj in _db['People'].items():
        try:
            int(person_id)
            val = transaction_dict[f"{person_obj['name']} {key}"][index]
            money_dict[person_obj['name']] = val
        except:
            continue
    return money_dict


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
    reset_db()
    df_db = pd.read_excel(xlsx_path, sheet_name=None)
    modded_db = {key: {} for key in df_db.keys()}
    # People (internal key) first
    modded_db['People'] = load_people_involved(df_db)
    modded_db['Summary'] = handle_loading_summary_sheet(df_db['Summary'])
    for key in df_db:
        if key not in ('Summary', 'People'):
            modded_db[key] = handle_transaction_sheets(df_db[key], key, modded_db)
    update_db(modded_db)
    return

##########################################################

def get_db() -> dict:
    return read_db()

def post_to_db(obj_to_add: dict, id: str, table: str) -> dict:
    db = read_db()
    db[table][id] = obj_to_add
    return update_db(db)

def patch_entire_table(table_data: dict, table: str) -> dict:
    db = read_db()
    db[table] = table_data
    return update_db(db)
