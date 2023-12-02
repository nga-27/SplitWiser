import json
from api import main

def get_all_status():
    status_dict = main.DB.get('Summary')
    return status_dict