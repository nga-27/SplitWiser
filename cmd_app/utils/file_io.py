""" File IO utilities for the cmd_app """
import os
import time
import shutil
from typing import Tuple, Union

from .constants import PrintColor


def error_handler(error_msg: str) -> None:
    """ Colorful way to print errors """
    print(f"{PrintColor.RED}ERROR: {error_msg}{PrintColor.NORMAL}")


def get_src_and_dest_paths(pwd: str) -> Tuple[Union[str, None], Union[str, None]]:
    """get_src_and_dest_paths

    Handle environment file settings and return file paths for moving the xlsx db file around

    Args:
        pwd (str): current working directory path

    Returns:
        Tuple[Union[str, None], Union[str, None]]: either (source, dest) paths or (None, None)
    """
    dot_env_path = os.path.join(pwd, '.env')
    if os.path.exists(dot_env_path) is False:
        error_handler(f'NO ENVIRONMENT FILE. Current PWD: {dot_env_path}')
        return None, None

    source_path = os.getenv("INPUT_SOURCE_PATH", "")
    dest_path = os.path.join(
        os.getenv("SHARE_DIRECTORY_PATH", ""), os.getenv("SPLIT_WISER_FILE", ""))
    return source_path, dest_path


def copy_from_cloud(pwd: str) -> bool:
    """copy_from_cloud

    Copies xlsx file from cloud-local location to repo for operations

    Args:
        pwd (str): current working dir path

    Returns:
        bool: if successful in copying from cloud location to this repo to operate on
    """
    source_path, dest_path = get_src_and_dest_paths(pwd)
    if source_path is None:
        return False
    shutil.copy(dest_path, source_path)
    time.sleep(1)
    return True


def push_to_cloud(pwd: str) -> bool:
    """push_to_cloud

    Copies xlsx file from the repo location to the cloud-local location

    Args:
        pwd (str): current working dir path

    Returns:
        bool: if successful in pushing updated xlsx file to cloud location
    """
    print("Pushing changes to the cloud...")
    source_path, dest_path = get_src_and_dest_paths(pwd)
    if source_path is None:
        return False
    shutil.copy(source_path, dest_path)
    time.sleep(1)
    return True
