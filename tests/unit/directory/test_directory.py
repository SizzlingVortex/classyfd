"""Contains the unit tests for the inner directory package"""

import unittest
import os
import tempfile

from classyfd import Directory, InvalidDirectoryValueError

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
    
  


if __name__ == "__main__":
    unittest.main()