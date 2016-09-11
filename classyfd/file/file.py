"""Contains a File class to represent real files"""

import os
import pathlib
import shutil
# Unix-like Only Imports
try:
    import pwd
    import grp
except ImportError:
    pass

from .. import config, utils
from ..base import _BaseFileAndDirectoryInterface
from ..exceptions import FileError, InvalidFileValueError


class File(_BaseFileAndDirectoryInterface):
    """A class that groups together the (meta)data and behavior of files"""
    def __init__(self, path):
        """
        Construct the object
        
        Parameters:
        path -- (str) where the file is (or will be) located at. An exception
                is raised if the path refers to a directory, and also if an
                empty string is given.
        
        """
        if not path:
            # No point in continuing since the methods of this class assume
            # that a path will be given upon instantiation.
            raise InvalidFileValueError("No file path was given")
        
        # Raise an exception if the path refers to a directory
        path_exists = os.path.exists(path)
        path_is_a_directory = os.path.isdir(path)
        if path_exists and path_is_a_directory:
            raise IsADirectoryError("The path refers to a directory")
        
        self._path = utils.normalize_path(os.path.abspath(path)) 
        return
    
    # Special Methods
    def __repr__(self):
        """Get the official string representation"""
        repr_ = (
            "{class_name}(\"{path}\")"
            .format(class_name=File.__name__, path=self.path)
        )
        return repr_
    
    def __str__(self):
        """Get the informal string representation"""
        return self.path
    
    # Properties
    @property
    def name(self):
        """
        Get the final part of the file's path (which includes any 
        filename extensions).
        
        Return Value:
        (str)
        
        """
        return pathlib.Path(self.path).name
    
    @property
    def path(self):
        """
        Get the absolute path (or location) of the file
        
        Return Value:
        (str)
        
        """
        return self._path  
    
    @path.setter
    def path(self, new_path):
        """
        Set the path of the file
        
        Parameters:
        new_path -- (str) the new path to assign. This can be an absolute or a
                    relative path.
        
        """
        # Raise an exception if the path refers to a directory
        path_exists = os.path.exists(new_path)
        path_is_a_directory = os.path.isdir(new_path)
        if path_exists and path_is_a_directory:
            raise IsADirectoryError("The path refers to a directory")
        
        self._path = utils.normalize_path(os.path.abspath(new_path))         
        return
    
    @property
    def exists(self):
        """
        Return whether the file exists or not
        
        Return Value:
        (bool)
        
        """
        return os.path.exists(self.path)
    
    @property
    def created_on(self):
        pass    
    
    @property
    def size(self):
        """
        Get the size of the file (in bytes)
        
        Return Value:
        (int)
        
        """
        return os.path.getsize(self.path) 
    
    @property
    def parent(self):
        """
        Get the parent directory of the file
        
        Return Value:
        (str)
        
        """
        return str(pathlib.Path(self.path).parent)  
    
    @property
    def owner(self):
        """
        Get the details of the user that owns the file
        
        Supported Operating Systems:
        Unix-like
        
        Return Value:
        user -- (dict) contains the details of the user that owns the file.
                Specifically, it contains the user's username, user_id, 
                group_id, and home directory. The keys are username, user_id,
                group_id, and directory.
        
        """
        if config._OPERATING_SYSTEM == "windows":
            raise NotImplementedError(
                "File.owner is not supported on Windows"
            ) 
        
        # Get the owner's details from the user account and password database
        pwd_user = pwd.getpwnam(pathlib.Path(self.path).owner())
        
        user = {}
        user["username"] = pwd_user.pw_name
        user["user_id"] = pwd_user.pw_uid
        user["group_id"] = pwd_user.pw_gid
        user["directory"] = pwd_user.pw_dir
        
        return user
    
    @property
    def group(self):
        """
        Get the details of the group that owns the file
        
        Supported Operating Systems:
        Unix-like
        
        Return Value:
        group -- (dict) contains the details for the group that owns the file.
                 Specifically, it contains the group's id, name, and its
                 members. Its keys are id, name, and members.
        
        """
        if config._OPERATING_SYSTEM == "windows":
            raise NotImplementedError(
                "File.group is not supported on Windows"
            )       
        
        # Get the group's details from the group database
        grp_group = grp.getgrnam(pathlib.Path(self.path).group())
        
        group = {}
        group["name"] = grp_group.gr_name
        group["id"] = grp_group.gr_gid
        group["members"] = grp_group.gr_mem
        
        return group
    
    @property
    def stem(self):
        """
        Get the file's final path component, excluding its extension.
        
        In the event the file has multiple extensions, only the final extension
        is removed.
        
        Return Value:
        (str)
        
        """
        return pathlib.Path(self.path).stem
    
    @property
    def extension(self):
        """
        Get the file's extension
        
        In the event a file has multiple extensions, then only the final
        extension is returned.
        
        Return Value:
        (str)
        
        """
        return pathlib.Path(self.path).suffix
    
    @property
    def extensions(self):
        """
        Get all of the file's extensions

        Return Value:
        (list)
        
        """
        return pathlib.Path(self.path).suffixes    
    
    @property
    def is_file(self):
        """
        Whether the object's path refers to a file or not
        
        Normally, this method shouldn't need to be used since checks are made
        on a given path when a File object is created and if its value changes
        later. However, this method becomes useful in any situation when one 
        isn't sure a path will always refer to a file. For example, when a
        directory replaces a file (with the same path) on the file system, 
        all after a File object is created.
        
        """
        return os.path.isfile(self.path)
    
    # Regular Methods
    def get_parent(self, levels=1):
        """
        Get the parent directory of the file
        
        Parameters:
        levels -- (int) how many levels to look upwards for a parent directory.
                  For example, 1 represents the immediate directory that
                  contains the file. For clarity, 0 is treated the same as 1
                  in this method.
        
        Return Value:
        (str)
        
        """
        if levels < 0:
            raise InvalidFileValueError("levels should be 0 or more")
        
        elif levels == 0:
            # 0 and 1 should be treated the same for clarity
            levels = 1
        
        p = pathlib.Path(self.path)        
        for i in range(levels):
            parent = str(p.parent)
            p = pathlib.Path(parent)
               
        return parent         
    
    def create(self):
        pass         
    
    def get_permissions(self):
        pass  
    
    def change_permissions(self):
        pass      
    
    def chmod(self):
        pass 
    
    def change_owner(self, user):
        """
        Change the owner of the file
        
        Parameters:
        username -- (str or int) the username or ID that should own the file
        
        Supported Operating Systems:
        Unix-like
        
        """
        if config._OPERATING_SYSTEM == "windows":
            raise NotImplementedError(
                "File.change_owner() is not supported on Windows"
            )
        
        shutil.chown(self.path, user=user)
        
        return        
    
    def change_group(self, group):
        """
        Change the group of the file
        
        Parameters:
        group -- (str or int) the group name or ID that should own the file

        Supported Operating Systems:
        Unix-like

        """        
        if config._OPERATING_SYSTEM == "windows":
            raise NotImplementedError(
                "File.change_group() is not supported on Windows"
            )
        
        shutil.chown(self.path, group=group)
        
        return                    
    
    def copy(self):
        pass
    
    def move(self, directory, new_file_name=None, replace_existing_file=False):
        """
        Move the file
        
        Parameters:
        directory -- (str) the directory to move the file into
        new_file_name -- (str) if given, the file's name will be renamed to 
                         this. This should just be the new name of the file
                         (including any file extensions), so no paths.
        replace_existing_file (bool) if the path of the new file name already
                              exists, then this variable determines what action
                              to take. If False, then a FileExistsError is 
                              raised. If True, then the existing file gets
                              replaced with this one.
        
        """
        self._execute_rename(
            directory, new_file_name=new_file_name, 
            replace_existing_file=replace_existing_file
        )
        
        return
    
    def rename(self, new_file_name, replace_existing_file=False):
        """
        Rename the file (the file's name including any file extensions)
        
        This method is only meant to change the file's name, not any other part
        of the file's path. For that type of behavior (like GNU mv), use the
        "move" method instead.
        
        Parameters:
        new_file_name -- (str) what to rename the file to. This should include
                         any file extensions. An exception will be raised
                         if any slashes are included because this method will
                         think the value is that of a path rather than a
                         file name only.                         
        replace_existing_file -- (bool) if the path of the new file name already
                                  exists, then this variable determines what 
                                  action to take. If False, then a 
                                  FileExistsError is raised. If True, then the
                                  existing file gets replaced with this one.
        
        """
        DIRECTORY = self.parent
        
        self._execute_rename(
            DIRECTORY, new_file_name=new_file_name, 
            replace_existing_file=replace_existing_file
        )
        
        return
    
    def remove(self):
        """Remove (delete) the file"""
        os.remove(self.path)
        return
    
    def open(self, *args, **kwargs):
        """
        Open the file and return a standard Python file object
        
        This method is a wrapper for Python's built-in open() function.
        Therefore, when using it, it should feel nearly the same as using
        Python's open() itself. The only real difference is that no path to a 
        file should be given as an argument since this method takes care of that
        internally.
        
        Generally speaking, this method is not meant to replace the use of
        Python's open() function. It is, however, provided as a convenience
        method -- and should be used when one needs to perform operations on a
        file (that an instance of this class refers to) in the same way that one
        would if they were just using Python's open() function.
        
        Parameters:
        The same arguments that Python's built-in open() function takes
        can be used here as well.
        
        Return Value:
        A standard Python file object (text file, raw binary file, or a 
        buffered binary file).
        
        More Information:
        As this is just a wrapper for Python's built-in open() function,
        please see Python's documentation for what else this method can do.
        
        """
        return open(self.path, *args, **kwargs)
    
    # Private Methods
    def _execute_rename(self, directory, new_file_name=None,
                        replace_existing_file=False):
        """
        Execute a file rename (or move) operation
        
        This method was created to contain the common code between the .rename()
        and .move() methods because they share a lot of the same logic.
        
        Parameters:
        directory -- (str) the directory the file should be in
        new_file_name -- (str) the file's name will be renamed to 
                         this. This should just be the new name of the file
                         (including any file extensions), so no paths.
        replace_existing_file -- (bool) if the path of the new file name already
                                 exists, then this variable determines what 
                                 action to take. If False, then a 
                                 FileExistsError is raised. If True, then the
                                 existing file gets replaced with this one.
        
        """
        SLASHES = ("\\", "/")         
        if new_file_name and any(c in new_file_name for c in SLASHES):
            # The new file name is likely a path, rather than just a file name.
            raise InvalidFileValueError(
                "Slashes are not allowed in the new file name"
            )       
        
        if new_file_name:
            new_file_path = os.path.join(directory, new_file_name)
        else:
            new_file_path = os.path.join(directory, self.name)
        
        file_already_exists = os.path.exists(new_file_path)
        if file_already_exists and not replace_existing_file:
            raise FileExistsError(
                "Cannot rename the file because a file with the chosen name "
                "already exists"
            )         
        
        elif file_already_exists and replace_existing_file:
            # os.replace() is the Python-recommended way of doing cross-platform
            # file replaces, rather than os.rename().
            os.replace(self.path, new_file_path)
        
        else:
            # Perform a simple "rename" operation since the new file path does
            # not already exist.
            os.rename(self.path, new_file_path)           
                    
        # Update the path
        self.path = new_file_path        
        return