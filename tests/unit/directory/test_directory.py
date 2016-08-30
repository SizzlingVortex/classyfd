"""Contains the unit tests for the inner directory package"""

import unittest
import os
import tempfile
import pathlib

from classyfd import Directory, InvalidDirectoryValueError, utils

class TestDirectory(unittest.TestCase):
    def setUp(self):
        self.fake_path = os.path.abspath("hello-world-dir")
        return
    
    def test_create_directory_object(self):
        d = Directory(self.fake_path)
        self.assertTrue(d)
        return
    
    def test_raise_exception_for_empty_str_path_when_creating_dir_object(self):
        self.assertRaises(InvalidDirectoryValueError, Directory, "")
        return    
    
    def test_raise_exception_when_path_is_an_existing_file(self):
        with tempfile.NamedTemporaryFile() as tf:
            self.assertRaises(NotADirectoryError, Directory, tf.name)
        
        return
    
    def test_get_path(self):
        """
        A normalized, absolute path should be returned, even if a relative path
        is originally given when the instance object is created.
    
        """
        # Pass an Absolute Path
        d = Directory(self.fake_path)
        self.assertEqual(
            d.path, self.fake_path, msg="The absolute paths were not equal"
        )
    
        # Pass Relative Paths
        #
        # Assign fake directory paths
        relative_paths = ["./hello-world-dir", "../goodbye-world-dir"]
        absolute_paths = [os.path.abspath(p) for p in relative_paths]
        for i, path in enumerate(relative_paths):
            d = Directory(path)
            with self.subTest(path=path):
                self.assertEqual(
                    d.path, absolute_paths[i]
                ) 
                
        # Pass a Relative, Non-Normalized Path
        non_normalized_path = "//directory1\\directory2\\directory3"
        expected_path = utils.normalize_path(
            os.path.abspath(non_normalized_path)
        )
        
        d = Directory(non_normalized_path)
        self.assertEqual(
            d.path, expected_path, 
            msg="The relative, non-normalized path assert failed"
        )         
    
    
        return   
    
    def test_repr(self):
        """Test the official string representation of an instance"""
        d = Directory(self.fake_path)
        expected_repr = (
            '{class_name}("{path}")'
            .format(class_name=Directory.__name__, path=d.path)
        )
        self.assertEqual(repr(d), expected_repr)
        return    
    
    def test_str(self):
        """Test the informal string representation of an instance"""
        self.fake_path = os.path.abspath("hello-world/")
        d = Directory(self.fake_path)
        self.assertEqual(str(d), self.fake_path)
        return  
    
    def test_get_name(self):
        d = Directory(self.fake_path)
        expected_name = pathlib.Path(self.fake_path).name
        self.assertEqual(d.name, expected_name)
        return
    
    def test_get_parent_directory_path(self):
        # One level up
        fake_path = "/home/someuserthatdoesntexist/Documents"
        d = Directory(fake_path)
        expected_parent = os.path.abspath(
            "/home/someuserthatdoesntexist"
        )
        
        self.assertEqual(
            d.parent, expected_parent, msg="One level up assert failed"
        )
        
        # Zero should be treated the same as one level up
        expected_parent = os.path.abspath(
            "/home/someuserthatdoesntexist"
        )
        
        self.assertEqual(
            d.get_parent(levels=0), expected_parent,
            msg="Zero should be treated the same as one level up"
        )          
        
        # Two levels up
        expected_parent = os.path.abspath("/home")
        self.assertEqual(
            d.get_parent(levels=2), expected_parent,
            msg="Two levels up assert failed"
        )      
        
        return
    


if __name__ == "__main__":
    unittest.main()