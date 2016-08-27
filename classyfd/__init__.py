"""
ClassyFD is a Python library that makes working with files and directories
quick and easy. For example, rather than using many functions that are
scattered throughout different modules, ClassyFD provides custom classes that
group together (or encapsulate) the data and behavior of objects that represent
real files and directories. Additionally, ClassyFD provides sane and sensible 
defaults on its provided file and directory operations.

ClassyFD is written in pure Python, and its only dependency is the Python 
Standard Library.

Supported Versions of Python:
Python 3.4.x (and higher)

Copyright 2016 by Joshua Goring
License: MIT, see LICENSE for more details.


"""

__author__ = "Joshua Goring"
__version__ = ""
__license__ = "MIT"
__copyright__ = "Copyright 2016 Joshua Goring"


# The Public API
from .file import File
from .exceptions import (
    Error, FileError, InvalidFileValueError, DirectoryError, 
    InvalidDirectoryValueError
)