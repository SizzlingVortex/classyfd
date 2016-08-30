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
        repr_ = (
            "{class_name}(\"{path}\")"
            .format(class_name=Directory.__name__, path=self.path)
        )
        return repr_

    def __str__(self):
        return self.path
    
    # Properties
    @property
    def name(self):
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
        pass  
    
    @property
    def owner(self):
        pass  
    
    @property
    def group(self):
        pass   
    
    # Regular Methods
    def get_parent(self):
        pass         
    
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