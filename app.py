""" proto app as well as initial operator against the api """
import os
import subprocess
import threading
import time
import shutil

from dotenv import load_dotenv
from colorama import just_fix_windows_console

from cmd_app.main_handler import (
    run, startup, shutdown, get_src_and_dest_paths, boot_up, error_handler
)

just_fix_windows_console()
load_dotenv()

PARTIAL_BASE = os.getenv("PARTIAL_BASE_URL", "http://localhost:")
PORT_NUMBER = os.getenv("API_PORT_NUMBER", "8765")
BASE_URL = PARTIAL_BASE + PORT_NUMBER
PWD = os.path.dirname(__file__)

def copy_from_cloud() -> bool:
    source_path, dest_path = get_src_and_dest_paths(PWD)
    if source_path is None:
        return False
    shutil.copy(dest_path, source_path)
    time.sleep(1)
    return True

def push_to_cloud() -> bool:
    print("Pushing changes to the cloud...")
    source_path, dest_path = get_src_and_dest_paths(PWD)
    if source_path is None:
        return False
    shutil.copy(source_path, dest_path)
    time.sleep(1)
    return True


def run_api():
    subprocess.run(["uvicorn", "api.server:app", "--log-level=warning", f"--port={PORT_NUMBER}"])


def run_cmd_prompts():
    startup(BASE_URL)
    run(BASE_URL)
    shutdown(BASE_URL)


def run_main():
    boot_up()
    is_successful = copy_from_cloud()
    if not is_successful:
        error_handler("Missing path files. Exiting...")
        time.sleep(2)
        return

    t_api = threading.Thread(target=run_api, name='API')
    t_ui = threading.Thread(target=run_cmd_prompts, name='Command-Based UI')

    t_api.start()
    time.sleep(0.1)
    t_ui.start()

    t_ui.join()
    t_api.join()

    is_successful = push_to_cloud()
    if not is_successful:
        error_handler("Copying to cloud issue.")
        return

    time.sleep(1)
    print("Goodbye!")
    time.sleep(2)
    

if __name__ == "__main__":
    run_main() 
