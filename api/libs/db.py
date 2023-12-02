import pandas as pd

def handle_loading_summary_sheet(raw_df: pd.DataFrame) -> dict:
    sub_dict = {key: {} for key in raw_df.keys()}
    sub_dict.pop('Person')
    for key in sub_dict:
        for item, value in raw_df[key].items():
            sub_dict[key][raw_df['Person'][item]] = value
    return sub_dict


def load_people_involved(raw_df: pd.DataFrame) -> dict:
    sub_dict = {
        person_id: person_name for person_id, person_name in raw_df['Summary']['Person'].items()
    }
    return sub_dict


def handle_transaction_sheets(raw_df: pd.DataFrame, sheet_name: str) -> dict:
    trans_dict = {}
    
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
            modded_db[key] = handle_transaction_sheets(df_db[key], key)
    return modded_db