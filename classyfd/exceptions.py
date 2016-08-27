"""Contains all of the custom exceptions"""

class Error(Exception):
    """The base exception class for the package"""
    pass

# File Exceptions
class FileError(Error):
    """Raised when there are issues with custom File objects"""
    pass

class InvalidFileValueError(FileError):
    """Raised when an invalid value is passed to a File object's method, 
    regardless of the value's data type."""
    pass

# Directory Exceptions
class DirectoryError(Error):
    """Raised when there are issues with custom Directory objects"""
    pass

class InvalidDirectoryValueError(DirectoryError):
    """Raised when an invalid value is passed to a Directory object's method, 
    regardless of the value's data type."""
    pass