import shutil
import os
from typing import Dict
import datetime

import pandas as pd

from api.models.models import Transaction


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


def handle_transaction_sheets(raw_df: pd.DataFrame, _db: dict) -> dict:
    trans_dict = {}
    raw_df.dropna(inplace=True)
    df_as_dict = raw_df.to_dict()
    for i in range(len(df_as_dict['Date'])):
        date_val = df_as_dict['Date'][i]
        if not isinstance(date_val, str):
            date_val = date_val.strftime("%m/%d/%Y")

        transaction = Transaction(
            id=str(i),
            date=date_val,
            item=df_as_dict['Transaction Item'][i],
            paid_by_id=money_by_involved_handler(df_as_dict, i, 'Paid', _db),
            owed_by_id=money_by_involved_handler(df_as_dict, i, 'Owes', _db)
        )
        trans_dict[str(i)] = transaction.dict()
    return trans_dict


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


def convert_db_trans_to_xlsx_trans(db_table: dict) -> pd.DataFrame:
    COLUMNS = ['Date', 'Transaction Item', 'Jill Paid', 'Nick Paid', 'Jill Owes', 'Nick Owes']
    df_as_dict = {col: [] for col in COLUMNS}
    for _, trans in db_table.items():
        df_as_dict['Date'].append(trans['date'])
        df_as_dict['Transaction Item'].append(trans['item'])
        df_as_dict['Jill Paid'].append(trans['paid_by_id']['Jill'])
        df_as_dict['Nick Paid'].append(trans['paid_by_id']['Nick'])
        df_as_dict['Jill Owes'].append(trans['owed_by_id']['Jill'])
        df_as_dict['Nick Owes'].append(trans['owed_by_id']['Nick'])
    df_db = pd.DataFrame.from_dict(df_as_dict)
    df_db.set_index('Date', inplace=True)
    return df_db


def convert_db_people_to_xlsx_people(person_table: dict) -> pd.DataFrame:
    COLUMNS = ["Person", "Total", "House Avery", "Jill and Nick"]
    df_as_dict = {col: [] for col in COLUMNS}
    for col in COLUMNS:
        if col == 'Person':
            df_as_dict[col] = [name for name in person_table['Total']]
        else:
            df_as_dict[col] = [val for _, val in person_table[col].items()]
    df_db = pd.DataFrame.from_dict(df_as_dict)
    df_db.set_index('Person', inplace=True)
    return df_db


###########################################################

def find_max_column_width(column: list, column_name: str='') -> int:
    """find_max_column_width

    Of all items in a given column list, find the "longest" item (when casted to a string) so we
    can format the column widths appropriately.

    Args:
        column (list): column to evaluate each item for width by casting item to str and measuring
        column_name (str): name of the column (Default: '')

    Returns:
        int: max length of column + 2
    """
    max_len = len(column_name)
    for item in column:
        if len(str(item)) > max_len:
            max_len = len(str(item))

    return max_len + 2


###########################################################


def get_real_xlsx_db(xlsx_path: str) -> dict:
    df_db = pd.read_excel(xlsx_path, sheet_name=None)
    modded_db = {key: {} for key in df_db.keys()}
    # People (internal key) first
    modded_db['People'] = load_people_involved(df_db)
    modded_db['Summary'] = handle_loading_summary_sheet(df_db['Summary'])
    for key in df_db:
        if key not in ('Summary', 'People'):
            modded_db[key] = handle_transaction_sheets(df_db[key], modded_db)
    return modded_db


def set_real_xlsx_db(db_dict: dict, db_path: str) -> None:
    SHEETS = ['Summary', 'House Avery', 'Jill and Nick', 'Archived - House Avery', 'Archived - Jill and Nick']
    xlsx_as_dict = {sheet: {} for sheet in SHEETS}
    with pd.ExcelWriter(db_path) as writer:  
        for sheet in SHEETS:
            if sheet not in ('Summary'):
                xlsx_as_dict[sheet] = convert_db_trans_to_xlsx_trans(db_dict[sheet])
            else:
                xlsx_as_dict[sheet] = convert_db_people_to_xlsx_people(db_dict[sheet])
            xlsx_as_dict[sheet].to_excel(writer, sheet_name=sheet)

            worksheet = writer.sheets[sheet]
            max_len = find_max_column_width(
                xlsx_as_dict[sheet].index, column_name=xlsx_as_dict[sheet].index.name)
            worksheet.set_column(0, 0, max_len)

            for i, col in enumerate(xlsx_as_dict[sheet]):
                max_len = find_max_column_width(xlsx_as_dict[sheet][col], col)
                worksheet.set_column(i+1, i+1, max_len)


def archive_xlsx_file(src_path: str) -> None:
    current_timestamp = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    new_path = f"{current_timestamp}.xlsx"
    new_dir = os.path.join("output", "archive")
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    new_path = os.path.join(new_dir, new_path)
    shutil.copy(src_path, new_path)
