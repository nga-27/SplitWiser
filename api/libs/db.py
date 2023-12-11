import os
import json
from typing import Dict

from api.libs.xlsx import get_real_xlsx_db, set_real_xlsx_db, archive_xlsx_file


DB_DIR = "__internal__"
DB_PATH = os.path.join(DB_DIR, "db.json")


###########################################

def update_db(db_obj: dict):
    with open(DB_PATH, 'w') as dbf:
        json.dump(db_obj, dbf)
    return

def read_db():
    db_obj = {}
    with open(DB_PATH, 'r') as dbf:
        db_obj = json.load(dbf)
    return db_obj

##########################################################

def save_db(db_path: str):
    db = read_db()
    set_real_xlsx_db(db, db_path)


def reset_db():
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
    with open(DB_PATH, 'w') as db_file:
        # wipe the old temp db clean!
        json.dump({}, db_file)
    return

# Public-facing init_db structure for managing functionality
def init_db(xlsx_path: str) -> None:
    reset_db()
    modded_db = get_real_xlsx_db(xlsx_path)
    update_db(modded_db)
    return

def get_db() -> Dict[str, dict]:
    return read_db()

def post_to_db(obj_to_add: dict, table: str) -> None:
    db = read_db()
    db_num_records = len(db[table])
    for _id in range(db_num_records - 1, -1, -1):
        db[table][str(_id)]['id'] = str(_id + 1)
        db[table][str(_id + 1)] = db[table][str(_id)]
    db[table]['0'] = obj_to_add
    return update_db(db)

def patch_entire_table(table_data: dict, table: str) -> None:
    db = read_db()
    db[table] = table_data
    return update_db(db)

def archive_db(src_path: str) -> None:
    archive_xlsx_file(src_path)

def reorder_table(table: str) -> None:
    db = read_db()
    table_data = db[table]
    updated_table = {}
    counter = 0
    for _, record in table_data.items():
        updated_table[str(counter)] = record
        counter += 1
    db[table] = updated_table
    return update_db(db)

