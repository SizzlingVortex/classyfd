"""Contains a Directory class to represent real directories"""

import os
import pathlib

from ..base import _BaseFileAndDirectoryInterface
from ..exceptions import InvalidDirectoryValueError
from .. import utils


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
        Get the absolute path (or location) of the file
        
        Return Value:
        (str)
        
        """
        return self._path              
    
    @property
    def exists(self):
        pass
    
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
        pass  
    
    @property
    def group(self):
        pass   
    
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
    
    def change_owner(self):
        pass       
    
    def change_group(self):
        pass             
    
    def copy(self):
        pass
    
    def move(self):
        pass
    
    def rename(self):
        pass 
    
    def remove(self):
        pass    