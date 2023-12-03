import os
from typing import List
import pandas as pd

from api.models.models import Transaction, TransactionalDebt

INTERNAL_DIR = "__internal__"


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
    return sub_dict

def money_by_involved_handler(transaction_dict: dict, index: int, key: str, _db: dict) -> List[dict]:
    money_list = []
    if key not in ('Owes', 'Paid'):
        return money_list
    for person_id, person_obj in _db['People'].items():
        try:
            int(person_id)
            val = transaction_dict[f"{person_obj['name']} {key}"][index]
            money_list.append({person_id: val})
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
        print(transaction)
    return raw_df

##########################################################

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
