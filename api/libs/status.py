import json
from api import main

def get_all_status():
    status = main.DB.get('Summary')
    status.dropna(inplace=True)
    status_dict = status.to_dict()
    return status_dict