import os
import sys

from multiprocessing import freeze_support
import pprint

# forced import hints for pyinstaller (for one day making this an application)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def load_db() -> dict:
    from dotenv import load_dotenv
    from api.libs.db import init_db
    DOTENV_PATH = os.path.join(os.getcwd(), '..','.env')
    load_dotenv(DOTENV_PATH)
    db_path = os.path.join('..', os.getenv("INPUT_SOURCE_PATH"))
    db = init_db(db_path)
    pprint.pprint(db)
    return db

DB = load_db()

def run_main():
    import uvicorn
    uvicorn.run("server:app", host="localhost", port=8765, reload=True, workers=1)

if __name__ == "__main__":
    run_main()    
