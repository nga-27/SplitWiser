import os
import time
import shutil
from typing import Tuple, Union

from .constants import PrintColor


def error_handler(msg: str) -> None:
    print(f"{PrintColor.RED}ERROR: {msg}{PrintColor.NORMAL}")


def get_src_and_dest_paths(pwd: str) -> Tuple[Union[str, None], Union[str, None]]:
    dot_env_path = os.path.join(pwd, '.env')
    if os.path.exists(dot_env_path) is False:
        error_handler(f'NO ENVIRONMENT FILE. Current PWD: {dot_env_path}')
        return None, None

    source_path = os.getenv("INPUT_SOURCE_PATH", "")
    dest_path = os.path.join(os.getenv("SHARE_DIRECTORY_PATH", ""), os.getenv("SPLIT_WISER_FILE", ""))
    return source_path, dest_path


def copy_from_cloud(pwd: str) -> bool:
    source_path, dest_path = get_src_and_dest_paths(pwd)
    if source_path is None:
        return False
    shutil.copy(dest_path, source_path)
    time.sleep(1)
    return True

def push_to_cloud(pwd: str) -> bool:
    print("Pushing changes to the cloud...")
    source_path, dest_path = get_src_and_dest_paths(pwd)
    if source_path is None:
        return False
    shutil.copy(source_path, dest_path)
    time.sleep(1)
    return True