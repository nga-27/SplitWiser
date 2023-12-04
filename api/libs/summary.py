from api.libs.db import get_db, patch_entire_table


def consolidate_debts(table_of_trans: dict) -> dict:
    """ output will be {name: amt, name: amt}, where one is 0.0 """
    jill_owes = 0.0
    nick_owes = 0.0
    for _, trans in table_of_trans.items():
        jill_owes += trans['owed_by_id']['Jill']
        nick_owes += trans['owed_by_id']['Nick']
    if jill_owes > nick_owes:
        jill_owes -= nick_owes
        nick_owes = 0.0
    else:
        nick_owes -= jill_owes
        jill_owes = 0.0
    return {"Jill": round(jill_owes, 2), "Nick": round(nick_owes, 2)}

def consolidate_debts_across_summary_table(summary_table: dict) -> dict:
    """ output will be for 'Total' key """
    nick_owes = summary_table['House Avery']['Nick'] + summary_table['Jill and Nick']['Nick']
    jill_owes = summary_table['House Avery']['Jill'] + summary_table['Jill and Nick']['Jill']
    if jill_owes > nick_owes:
        jill_owes -= nick_owes
        nick_owes = 0.0
    else:
        nick_owes -= jill_owes
        jill_owes = 0.0
    return {"Jill": round(jill_owes, 2), "Nick": round(nick_owes, 2)}


def get_all_summary():
    summary_dict = get_db().get('Summary')
    return summary_dict

def update_summary():
    full_db = get_db()
    full_db['Summary']['House Avery'] = consolidate_debts(full_db['House Avery'])
    full_db['Summary']['Jill and Nick'] = consolidate_debts(full_db['Jill and Nick'])
    full_db['Summary']['Total'] = consolidate_debts_across_summary_table(full_db['Summary'])
    patch_entire_table(full_db['Summary'], 'Summary')
