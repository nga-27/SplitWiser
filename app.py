""" proto app as well as initial operator against the api """
import os
import subprocess
import threading
import time
import requests

from dotenv import load_dotenv
from colorama import just_fix_windows_console

from cmd_app.main_handler import run, startup, shutdown

just_fix_windows_console()
load_dotenv()

PARTIAL_BASE = os.getenv("PARTIAL_BASE_URL", "http://localhost:")
PORT_NUMBER = os.getenv("API_PORT_NUMBER", "8765")
BASE_URL = PARTIAL_BASE + PORT_NUMBER

def run_api():
    subprocess.run(["uvicorn", "api.server:app", "--log-level=warning", f"--port={PORT_NUMBER}"])

def run_cmd_prompts():
    startup(BASE_URL)
    run(BASE_URL)
    shutdown(BASE_URL)

def run_main():
    t_api = threading.Thread(target=run_api, name='API')
    t_ui = threading.Thread(target=run_cmd_prompts, name='Command-Based UI')

    t_api.start()
    time.sleep(0.1)
    t_ui.start()

    t_ui.join()
    t_api.join()
    print("Goodbye!")
    time.sleep(2)
    

if __name__ == "__main__":
    run_main() 
