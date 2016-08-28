"""
Contains utility functions used within this library that are also useful 
outside of it.

"""

import os
import pwd
import string
import random
import re


# Operating System Functions
def determine_if_os_is_posix_compliant():
    """
    Determine if the operating system is POSIX compliant or not
    
    Return Value:
    (bool)
    
    """
    return bool(os.name == "posix")


def determine_if_running_as_root_user():
    """
    Determine if the user running Python is "root" or not
    
    Supported Operating Systems:
    Unix-like
    
    Return Value:
    (bool)
    
    """
    # 0 is the UID used for most Unix-like systems for the root user. In the
    # event that it's not, another check is done to see if the username is 
    # "root".    
    #
    # For an explanation on why os.geteuid was used, instead of os.getuid, 
    # see: http://stackoverflow.com/a/14951764
    is_running_as_root = bool(
        os.geteuid() == 0 or 
        pwd.getpwuid(os.geteuid()).pw_name.lower() == "root"
    )
    
    return is_running_as_root

# File Functions
def get_random_file_name(directory):
    """
    Generate a random, unique file name of 32 characters
    
    The generated file name may include lowercase letters and numbers.
    
    Parameters:
    directory -- (str) the directory the file will be in. This will determine
                 the unique name given to it.
    
    Return Value:
    random_file_name -- (str) this is just a randomly generated file name, so
                        the full/absolute path is not included.
    
    """
    CHARACTER_LENGTH = 32
    NUMBERS = string.digits
    LETTERS = string.ascii_lowercase
    VALID_CHARACTERS = tuple(LETTERS + NUMBERS)
    
    while True:
        random_file_name = ""
        for i in range(CHARACTER_LENGTH):
            random_file_name += random.choice(VALID_CHARACTERS)
        
        file_path_already_exists = os.path.exists(
            os.path.join(directory, random_file_name)
        )
        if file_path_already_exists:
            # Try again
            continue
        else:
            # Sweet, use the generated file name
            break
    
    return random_file_name


def normalize_path(path):
    """
    Normalize a file or directory's path
    
    This function is more strict than Python's os.path.normpath on Unix-like
    operating systems because only forward slashes are allowed to be returned
    (for Unix-like operating systems). However, on Windows, os.path.normpath
    was already strict enough, so this function acts the same on Windows.
    
    Parameters:
    path -- (str) the path to normalize
    
    Return Value:
    (str)
    
    """
    forward_slashes_regexp = re.compile(r"/{1,}")
    back_slashes_regexp = re.compile(r"\{1,}")    
    
    is_unix_like = determine_if_os_is_posix_compliant()
    if is_unix_like:
        normalized_path = os.path.normpath(path)
        # Perform extra operations since os.path.normpath isn't strict enough
        # on Unix-like operating systems.
        normalized_path = re.sub(forward_slashes_regexp, "/", normalized_path)
        normalized_path = re.sub(back_slashes_regexp, "/", normalized_path)
    else:
        normalized_path = os.path.normpath(path)
    
    return normalized_path