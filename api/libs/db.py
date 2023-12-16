""" DB Utilities for managing state and data manipulation between xlsx and json DBs """
import os
import json
from typing import Dict

from api.libs.xlsx import get_real_xlsx_db, set_real_xlsx_db, archive_xlsx_file


DB_DIR = "__internal__"
DB_PATH = os.path.join(DB_DIR, "db.json")


###########################################

def update_db(db_obj: dict) -> None:
    """update_db

    Low-level function that saves the json db snapshot to the json db file

    Args:
        db_obj (dict): dictionary version of the db snapshot to save
    """
    with open(DB_PATH, 'w', encoding='utf-8') as dbf:
        json.dump(db_obj, dbf)


def read_db() -> Dict[str, dict]:
    """read_db

    Low-level function that re-reads the data from the json db file and returns its contents as a
    real-time db snapshot

    Returns:
        Dict[str, dict]: json db copy, table names as top-level keys
    """
    db_obj = {}
    with open(DB_PATH, 'r', encoding='utf-8') as dbf:
        db_obj = json.load(dbf)
    return db_obj

##########################################################

def save_db(xlsx_db_path: str) -> None:
    """save_db

    Save the json db to the xlsx db file

    Args:
        db_path (str): xlsx db file path
    """
    _db = read_db()
    set_real_xlsx_db(_db, xlsx_db_path)


def reset_db() -> None:
    """reset_db

    Effectively erase the stored json db (no carry over is desired, esp for temporary files)
    """
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
    with open(DB_PATH, 'w', encoding='utf-8') as db_file:
        # wipe the old temp db clean!
        json.dump({}, db_file)


def init_db(xlsx_path: str) -> None:
    """init_db

    Convert and pull in the xlsx db data into the real-time json db

    Args:
        xlsx_path (str): path of the synced xlsx db file
    """
    reset_db()
    modded_db = get_real_xlsx_db(xlsx_path)
    update_db(modded_db)


def get_db() -> Dict[str, dict]:
    """get_db

    return a copy of the real-time DB

    Returns:
        Dict[str, dict]: the entire data base, table names as top-level keys
    """
    return read_db()


def post_to_db(obj_to_add: dict, table_name: str) -> None:
    """post_to_db

    Add a record to the DB [table]

    Args:
        obj_to_add (dict): new record to add
        table_name (str): table name
    """
    _db = read_db()
    db_num_records = len(_db[table_name])
    for _id in range(db_num_records - 1, -1, -1):
        _db[table_name][str(_id)]['id'] = str(_id + 1)
        _db[table_name][str(_id + 1)] = _db[table_name][str(_id)]
    _db[table_name]['0'] = obj_to_add
    update_db(_db)


def patch_entire_table(table_data: dict, table_name: str) -> None:
    """patch_entire_table

    Used after re-ordering the DB, typically after a payment or transaction addition

    Args:
        table_data (dict): entire table data in json format
        table_name (str): table name
    """
    _db = read_db()
    _db[table_name] = table_data
    update_db(_db)


def archive_db(src_path: str) -> None:
    """archive_db

    Args:
        src_path (str): archive the json db to the root xlsx db file
    """
    archive_xlsx_file(src_path)


def reorder_table(table_name: str) -> None:
    """reorder_table

    After a deletion occurs, we need to make sure we start at "0" again

    Args:
        table_name (str): table name
    """
    _db = read_db()
    table_data = _db[table_name]
    updated_table = {}
    counter = 0
    for _, record in table_data.items():
        updated_table[str(counter)] = record
        counter += 1
    _db[table_name] = updated_table
    update_db(_db)
