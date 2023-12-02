"""copier.py

So we can copy the league output to a shared drive!
"""
import os
import shutil
import argparse
from dotenv import load_dotenv


PWD = os.path.dirname(__file__)
DOTENV_PATH = os.path.join(PWD, '.env')
if os.path.exists(DOTENV_PATH) is False:
    print(f'WARNING: NO ENVIRONMENT FILE. Current PWD: {DOTENV_PATH}')

load_dotenv(DOTENV_PATH)

SOURCE_PATH = os.getenv("INPUT_SOURCE_PATH", "")
DEST_PATH = os.path.join(os.getenv("SHARE_DIRECTORY_PATH", ""), os.getenv("SPLIT_WISER_FILE", ""))


def local_to_google_sheets():
    """spreadsheet copier

    Since shell commands (such as "cp") are apparently terrible with paths, we'll do it in python!
    """
    shutil.copy(SOURCE_PATH, DEST_PATH)

def google_sheets_to_local():
    """spreadsheet copier

    Since shell commands (such as "cp") are apparently terrible with paths, we'll do it in python!
    """
    shutil.copy(DEST_PATH, SOURCE_PATH)

def copier(**kwargs):
    should_go_to_cloud = kwargs.get("local_to_cloud", False)
    if should_go_to_cloud:
        local_to_google_sheets()
    else:
        google_sheets_to_local()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate the JSON version of the schedule")
    parser.add_argument("--local_to_cloud", "-l", action='store_true', required=False, default=False)
    args = parser.parse_args()
    copier(**vars(args))