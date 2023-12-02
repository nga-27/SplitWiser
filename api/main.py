import os
import sys

import uvicorn
from multiprocessing import freeze_support
from dotenv import load_dotenv
import pandas as pd

# forced import hints for pyinstaller (one day)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def load_db():
    from api.libs.db import init_db
    DOTENV_PATH = os.path.join(os.getcwd(), '..','.env')
    load_dotenv(DOTENV_PATH)
    db_path = os.path.join('..', os.getenv("INPUT_SOURCE_PATH"))
    return init_db(db_path)

DB = load_db() #get_db()

def run_main():
    uvicorn.run("server:app", host="localhost", port=8765, reload=True, workers=1)

if __name__ == "__main__":
    run_main()    
