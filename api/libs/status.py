from api.libs.db import get_db

def get_all_status():
    status_dict = get_db().get('Summary')
    return status_dict