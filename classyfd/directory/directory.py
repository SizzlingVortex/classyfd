"""Contains a Directory class to represent real directories"""

import os
import pathlib
import shutil
# Unix-like Only Imports
try:
    import pwd
    import grp
except ImportError:
    pass

from ..base import _BaseFileAndDirectoryInterface
from ..exceptions import InvalidDirectoryValueError
from .. import utils, config


class Directory(_BaseFileAndDirectoryInterface):
    """A class that groups together the (meta)data and behavior of 
    directories"""
    def __init__(self, path):
        """
        Construct the object

        Parameters:
        path -- (str) where the directory is (or will be) located at. An 
                exception is raised if the path refers to a file, and also if an
                empty string is given.

        """
        if not path:
            # No point in continuing since the methods of this class assume
            # that a path will be given upon instantiation.
            raise InvalidDirectoryValueError("No directory path was given")
        
        # Raise an exception if the path refers to a file
        path_exists = os.path.exists(path)
        path_is_a_file = os.path.isfile(path)
        if path_exists and path_is_a_file:
            raise NotADirectoryError("The path refers to a file") 
        
        self._path = utils.normalize_path(os.path.abspath(path))         
        return
    
    # Special Methods
    def __repr__(self):
        """Get the official string representation"""
        repr_ = (
            "{class_name}(\"{path}\")"
            .format(class_name=Directory.__name__, path=self.path)
        )
        return repr_

    def __str__(self):
        """Get the informal string representation"""
        return self.path
    
    # Properties
    @property
    def name(self):
        """
        Get the name of the directory
        
        Return Value:
        (str)

        """        
        return pathlib.Path(self.path).name
    
    @property
    def path(self):
        """
        Get the absolute path (or location) of the directory
        
        Return Value:
        (str)
        
        """
        return self._path  
    
    @path.setter
    def path(self, new_path):
        """
        Set the path of the directory
        
        Parameters:
        new_path -- (str) the new path to assign. This can be an absolute or a
                    relative path.
        
        """
        # Raise an exception if the path refers to a file
        path_exists = os.path.exists(new_path)
        path_is_a_file = os.path.isfile(new_path)
        if path_exists and path_is_a_file:
            raise NotADirectoryError("The path refers to a file")
        
        self._path = utils.normalize_path(os.path.abspath(new_path))         
        return    
    
    @property
    def exists(self):
        return os.path.exists(self.path)
    
    @property
    def created_on(self):
        pass    
    
    @property
    def size(self):
        pass    
    
    @property
    def parent(self):
        """
        Get the parent directory of the directory

        Return Value:
        (str)

        """
        return str(pathlib.Path(self.path).parent)   
    
    @property
    def owner(self):
        """
        Get the details of the user that owns the directory

        Supported Operating Systems:
        Unix-like

        Return Value:
        user -- (dict) contains the details of the user that owns the directory.
                Specifically, it contains the user's username, user_id, 
                group_id, and home directory. The keys are username, user_id,
                group_id, and directory.

        """
        if config._OPERATING_SYSTEM == "windows":
            raise NotImplementedError(
                "Directory.owner is not supported on Windows"
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
        Get the details of the group that owns the directory

        Supported Operating Systems:
        Unix-like

        Return Value:
        group -- (dict) contains the details for the group that owns the 
                 directory. Specifically, it contains the group's id, name, and
                 its members. Its keys are id, name, and members.

        """
        if config._OPERATING_SYSTEM == "windows":
            raise NotImplementedError(
                "Directory.group is not supported on Windows"
            )       
    
        # Get the group's details from the group database
        grp_group = grp.getgrnam(pathlib.Path(self.path).group())
    
        group = {}
        group["name"] = grp_group.gr_name
        group["id"] = grp_group.gr_gid
        group["members"] = grp_group.gr_mem
    
        return group           
    
    @property
    def is_dir(self):
        """
        Whether the object's path refers to a directory or not
        
        Normally, this method shouldn't need to be used since checks are made
        on a given path when a Directory object is created and also if its value
        changes later. However, this method becomes useful in any situation when
        one isn't sure a path will always refer to a directory. For example, 
        when a file replaces a directory (with the same path) on the file 
        system, all after a Directory object is created.
        
        """
        return os.path.isdir(self.path)    
    
    # Regular Methods
    def get_parent(self, levels=1):
        """
        Get the parent directory of the directory
    
        Parameters:
        levels -- (int) how many levels to look upwards for a parent directory.
                  For example, 1 represents the immediate directory that
                  contains the directory referred to by the instance object. 
                  For clarity, 0 is treated the same as 1 in this method.
    
        Return Value:
        (str)
    
        """
        if levels < 0:
            raise InvalidDirectoryValueError("levels should be 0 or more")
    
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
        Change the owner of the directory
        
        Parameters:
        user -- (str or int) the username or ID that should own the directory
        
        Supported Operating Systems:
        Unix-like
        
        """
        if config._OPERATING_SYSTEM == "windows":
            raise NotImplementedError(
                "Directory.change_owner() is not supported on Windows"
            )
        
        shutil.chown(self.path, user=user)
        
        return        
               
    
    def change_group(self, group):
        """
        Change the group of the directory
        
        Parameters:
        group -- (str or int) the group name or ID that should own the directory

        Supported Operating Systems:
        Unix-like

        """        
        if config._OPERATING_SYSTEM == "windows":
            raise NotImplementedError(
                "Directory.change_group() is not supported on Windows"
            )
        
        shutil.chown(self.path, group=group)
        
        return                    
    
    def copy(self):
        pass
    
    def move(self):
        pass
    
    def rename(self, new_directory_name):
        """
        Rename the directory
        
        This method is only meant to change the directory's name, not any other
        part of its path. For that type of behavior (like GNU mv), use the
        "move" method instead.
        
        Parameters:
        new_directory_name -- (str) what to rename the directory to. An 
                              exception will be raised if any slashes are
                              included because this method will think the value
                              is that of a path rather than a new name for the
                              directory.

        
        """
        DIRECTORY = self.parent
        
        self._execute_rename(
            DIRECTORY, new_directory_name=new_directory_name
        )
        
        return
 
    
    def remove(self, empty_only=True):
        """
        Remove the directory
        
        Parameters:
        empty_only -- (bool) If True, then the directory is only removed if it
                      is empty. If False, then the directory and any files 
                      and sub-directories are deleted. 
        
        """
        if empty_only:
            os.rmdir(self.path)
        else:
            # Delete the directory and anything in it
            shutil.rmtree(self.path)
        
        return
    
    # Private Methods
    def _execute_rename(self, base_directory, new_directory_name=None):
        """
        Execute a file rename (or move) operation

        This method was created to contain the common code between the .rename()
        and .move() methods because they share a lot of the same logic.

        Parameters:
        base_directory -- (str) the parent directory of the directory that an
                          instance of this class refers to.
        new_directory_name -- (str) the file's name will be renamed to 
                              this. This should just be the new name of the file
                              (including any file extensions), so no paths.


        """
        # Initialize these for later (conditional) use
        path_refers_to_file = None
        path_refers_to_directory = None        
        
        SLASHES = ("\\", "/")         
        if new_directory_name and any(c in new_directory_name for c in SLASHES):
            # The new directory name is likely a path, rather than just a file
            # name.
            raise InvalidDirectoryValueError(
                "Slashes are not allowed in the new directory name"
            )       

        if new_directory_name:
            new_directory_path = (
                os.path.join(base_directory, new_directory_name)
            )
        else:
            new_directory_path = os.path.join(base_directory, self.name)

        path_already_exists = os.path.exists(new_directory_path)
        if path_already_exists:
            path_refers_to_file = os.path.isfile(new_directory_path)
            path_refers_to_directory = os.path.isdir(new_directory_path)        
        
        if path_already_exists:
            if path_refers_to_file:
                raise FileExistsError(
                    "Cannot rename the directory because a file with the chosen"
                    " name already exists"
                )
            elif path_refers_to_directory:
                raise IsADirectoryError(
                    "Cannot rename the directory because a directory with the "
                    "chosen name already exists"
                )        

        else:
            os.rename(self.path, new_directory_path)           

        # Update the path
        self.path = new_directory_path        
        return    