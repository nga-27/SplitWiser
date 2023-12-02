import pandas as pd


def init_db(xlsx_path: str) -> dict:
    df_db = pd.read_excel(xlsx_path, sheet_name=None)
    return df_db