import os
import shutil
from typing import Tuple

def delete_folder(path: str) -> bool:
    """
    Delete a folder and report success
    
    :param str path: The path of folder to delete
    :return: The success
    :rtype: bool
    """
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except:
            return False
        else:
            return True
    return True

def serialize_version(version: str) -> Tuple[int, int, int]:
    """
    Convert version string to tuple of integers
    
    :param str path: version in string
    :return: version in tuple
    :rtype: tuple
    """    
    return tuple(map(lambda e: int(e), version.split('.')))