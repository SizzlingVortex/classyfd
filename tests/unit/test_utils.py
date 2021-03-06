"""Contains the unit tests for the inner utils module"""

import unittest
import os
import re
import platform
from tempfile import NamedTemporaryFile, TemporaryDirectory
# Unix-like Only Imports
try:
    import pwd
except ImportError:
    pass

from classyfd import File, Directory, utils


# Globals
IS_UNIX_LIKE = bool(os.name == "posix")
OPERATING_SYSTEM = platform.system().lower()


# Tests
class TestUtils(unittest.TestCase):
    """Contains the cross-platform tests"""
    def test_if_os_is_posix_compliant(self):
        expected_result = bool(os.name == "posix")
        actual_result = utils.determine_if_os_is_posix_compliant()
        self.assertEqual(actual_result, expected_result)
        return
    
    def test_get_random_file_name(self):
        with NamedTemporaryFile() as tf:
            f = File(tf.name)
            directory = f.parent
        
        random_file_name = utils.get_random_file_name(directory)
        self.assertEqual(len(random_file_name), 32)
        
        random_file_path = os.path.join(directory, random_file_name)
        self.assertFalse(os.path.exists(random_file_path))
        
        return
    
    def test_get_random_directory_name(self):
        with TemporaryDirectory() as td:
            d = Directory(td)
            base_directory = d.parent
        
        random_directory_name = utils.get_random_directory_name(base_directory)
        self.assertEqual(len(random_directory_name), 32)
        
        random_directory_path = os.path.join(
            base_directory, random_directory_name
        )
        self.assertFalse(os.path.exists(random_directory_path))
        
        return
    
    

@unittest.skipUnless(IS_UNIX_LIKE, "Test supported on Unix-like systems only")
class TestUtilsUnixLike(unittest.TestCase):
    """Containst the tests specifically for Unix-like operating systems"""
    def test_if_running_as_root_user(self):
        expected_result = bool(
            os.geteuid() == 0 or 
            pwd.getpwuid(os.geteuid()).pw_name.lower() == "root"
        )
        actual_result = utils.determine_if_running_as_root_user()
        self.assertEqual(actual_result, expected_result)
        return   
    
    def test_normalize_path(self):
        non_normalized_path = "/home//sizzlingvortex\\Desktop\hello-world.txt"
        
        forward_slashes_regexp = re.compile(r"/{1,}")
        back_slashes_regexp = re.compile(r"\{1,}")        
        
        # For Unix-like operating systems, os.path.normpath is not srict enough
        # to generate the expected normalized path.
        expected_normalized_path = (
            re.sub(forward_slashes_regexp, "/", non_normalized_path)
        )
        
        expected_normalized_path = (
            re.sub(back_slashes_regexp, "/", expected_normalized_path)
        )
        
        # Normalize the Path        
        actual_normalized_path = utils.normalize_path(non_normalized_path)
        
        self.assertEqual(actual_normalized_path, expected_normalized_path)
        
        return   
    
    
@unittest.skipUnless(OPERATING_SYSTEM == "windows", "Windows-only test")    
class TestUtilsWindows(unittest.TestCase):
    """Contains the tests specifically for Windows"""
    def test_normalize_path(self):
        non_normalized_path = "C:/Users//sizzlingvortex\\Desktop\hello.txt"
        
        actual_normalized_path = utils.normalize_path(non_normalized_path)
        expected_normalized_path = os.path.normpath(non_normalized_path)
        
        self.assertEqual(actual_normalized_path, expected_normalized_path)
        
        return     


if __name__ == "__main__":
    unittest.main()