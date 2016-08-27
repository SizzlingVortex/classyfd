"""
Contains the base class that defines the main interface shared by both File and 
Directory objects.

"""

from abc import ABCMeta, abstractclassmethod


class _BaseFileAndDirectoryInterface(metaclass=ABCMeta):
    """Defines the main interface shared by both File and Directory objects"""
    # Special Methods
    @abstractclassmethod
    def __repr__(self):
        pass

    @abstractclassmethod
    def __str__(self):
        pass
    
    # Properties
    @property
    @abstractclassmethod
    def name(self):
        pass
    
    @property
    @abstractclassmethod
    def path(self):
        pass              
    
    @property
    @abstractclassmethod
    def exists(self):
        pass
    
    @property
    @abstractclassmethod
    def created_on(self):
        pass    
    
    @property
    @abstractclassmethod
    def size(self):
        pass    
    
    @property
    @abstractclassmethod
    def parent(self):
        pass  
    
    @property
    @abstractclassmethod
    def owner(self):
        pass  
    
    @property
    @abstractclassmethod
    def group(self):
        pass   
    
    # Regular Methods
    @abstractclassmethod
    def get_parent(self):
        pass         
    
    @abstractclassmethod
    def create(self):
        pass         
    
    @abstractclassmethod
    def get_permissions(self):
        pass  
    
    @abstractclassmethod
    def change_permissions(self):
        pass      
    
    @abstractclassmethod
    def chmod(self):
        pass 
    
    @abstractclassmethod
    def change_owner(self):
        pass       
    
    @abstractclassmethod
    def change_group(self):
        pass             
    
    @abstractclassmethod
    def copy(self):
        pass
    
    @abstractclassmethod
    def move(self):
        pass
    
    @abstractclassmethod
    def rename(self):
        pass 
    
    @abstractclassmethod
    def remove(self):
        pass     