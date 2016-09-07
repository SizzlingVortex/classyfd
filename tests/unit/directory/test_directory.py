"""Contains the unit tests for the inner directory package"""

import unittest
import os
import tempfile
import pathlib
import platform
# Unix-like Only Imports
try:
    import pwd
    import grp
except ImportError:
    pass

from classyfd import Directory, InvalidDirectoryValueError, utils, config


# Globals
OPERATING_SYSTEM = platform.system().lower()
IS_OS_POSIX_COMPLIANT = utils.determine_if_os_is_posix_compliant()

IS_UNIX_LIKE_ROOT_USER = None
if IS_OS_POSIX_COMPLIANT:
    # Determine if the User Running Python is "root" or not
    IS_UNIX_LIKE_ROOT_USER = utils.determine_if_running_as_root_user()
    

# Tests
class TestDirectory(unittest.TestCase):
    """Contains the cross-platform tests"""
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
    
    def test_set_path(self):
        # Absolute Path Given
        d = Directory(self.fake_path)
        # Reassign the same path
        d.path = self.fake_path
        self.assertEqual(
            d.path, self.fake_path, msg="The absolute path assert failed"
        )
        
        # Relative Path Given
        #
        # Change the path to just the directory's name
        d.path = d.name
        self.assertEqual(
            d.path, self.fake_path, msg="The relative path assert failed"
        )
        
        # Pass a Relative, Non-Normalized Path
        non_normalized_path = "directory1\\directory2\\hello-world.txt"
        expected_path = utils.normalize_path(
            os.path.abspath(non_normalized_path)
        )
        
        d = Directory(self.fake_path)
        d.path = non_normalized_path
        
        self.assertEqual(
            d.path, expected_path, 
            msg="The relative, non-normalized path assert failed"
        )          
        
        return   
    
    def test_raise_exception_for_setting_path_to_a_file(self):
        d = Directory(self.fake_path)
        with tempfile.NamedTemporaryFile() as tf:
            try:
                d.path = tf.name
            except NotADirectoryError:
                # Do nothing, as this is the right exception to be raised
                pass
            else:
                self.fail("A NotADirectoryError should have been raised")
        
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
    
    def test_raise_exception_for_get_parent_with_negative_values(self):
        d = Directory(self.fake_path)
        self.assertRaises(InvalidDirectoryValueError, d.get_parent, levels=-1)
        return    
    
    def test_is_a_directory(self):
        # Fake Path
        d = Directory(self.fake_path)
        self.assertFalse(d.is_dir, msg="The fake path assert failed")
        
        # A Real Directory
        with tempfile.TemporaryDirectory() as td:
            d = Directory(td)
            self.assertTrue(d.is_dir, msg="Real directory assert failed")
        
        # The Directory No Longer Exists
        with tempfile.TemporaryDirectory() as td:
            d = Directory(td)
        self.assertFalse(
            d.is_dir, msg="Directory no longer exists assert failed"
        )
            
        # Directory Path that Turns into a File Path
        #
        # First, create the directory
        with tempfile.TemporaryDirectory() as td:
            td_path = td
            d = Directory(td)
            self.assertTrue(d.is_dir)
        
        # The directory no longer exists
        self.assertFalse(d.is_dir)
        
        # Now create the file using the same path the directory had
        with open(td_path, mode="w", encoding=config._ENCODING):
            pass
        
        self.assertFalse(
            d.is_dir, 
            msg="Directory path turned file path assert failed"
        )
        self.assertTrue(
            os.path.isfile(td_path),
            msg="Directory path turned file path assert failed"
        )
        
        return   
    
    def test_remove_directory(self):
        # An Empty Directory
        td = tempfile.TemporaryDirectory()        
        with TemporaryDirectoryHandler(td):
            self.assertTrue(os.path.isdir(td.name))
            
            d = Directory(td.name)
            d.remove()
            self.assertFalse(
                os.path.exists(td.name), msg="Empty directory assert failed"
            )
        
        # A Non-Empty Directory
        td = tempfile.TemporaryDirectory()
        file = os.path.join(td.name, "hello-world.txt")
        # Create a file and a sub-directory
        with TemporaryDirectoryHandler(td):
            with open(file, mode="w", encoding=config._ENCODING):
                pass
            os.mkdir(os.path.join(td.name, "some-sub-directory"))
            d = Directory(td.name)
            d.remove(empty_only=False)
            self.assertFalse(
                os.path.exists(d.path), 
                msg="The non-empty directory assert failed"
            )
        
        return
    
    def test_raise_exception_for_removing_non_empty_directory(self):
        td = tempfile.TemporaryDirectory()
        file = os.path.join(td.name, "hello-world.txt")
        # Create a file and a sub-directory
        with TemporaryDirectoryHandler(td):
            with open(file, mode="w", encoding=config._ENCODING):
                pass
            os.mkdir(os.path.join(td.name, "some-sub-directory"))
            d = Directory(td.name)
            self.assertRaises(d.remove)        
        
        return
    
    def test_directory_exists(self):
        # The Directory Will not Exist
        d = Directory(self.fake_path)
        self.assertFalse(d.exists, msg="The directory should not exist")
        
        # The Directory Will Exist
        with tempfile.TemporaryDirectory() as td:
            d = Directory(td)
            self.assertTrue(d.exists, msg="The directory should exist")
        
        return    


@unittest.skipUnless(IS_OS_POSIX_COMPLIANT, "Unix-like only test")
class TestDirectoryUnixLike(unittest.TestCase):
    """Containst the tests specifically for Unix-like operating systems"""
    def test_get_owner_of_directory(self):
        
        with tempfile.TemporaryDirectory() as td:
            d = Directory(td)
            OWNER = pathlib.Path(d.path).owner()
            
            expected_owner_username = pwd.getpwnam(OWNER).pw_name
            self.assertEqual(
                d.owner["username"], expected_owner_username, 
                msg="The owner usernames are not equal"
            )
            
            expected_owner_user_id = pwd.getpwnam(OWNER).pw_uid
            self.assertEqual(
                d.owner["user_id"], expected_owner_user_id, 
                msg="The owner IDs are not equal"
            )
            
            expected_owner_group_id = pwd.getpwnam(OWNER).pw_gid
            self.assertEqual(
                d.owner["group_id"], expected_owner_group_id, 
                msg="The group IDs are not equal"
            )
            
            expected_owner_directory = pwd.getpwnam(OWNER).pw_dir
            self.assertEqual(
                d.owner["directory"], expected_owner_directory, 
                msg="The directories are not equal"
            )            
        
        return
    
    def test_get_group_of_directory(self):
        with tempfile.TemporaryDirectory() as td:
            d = Directory(td)
            GROUP = pathlib.Path(d.path).group()
            
            expected_group_name = grp.getgrnam(GROUP).gr_name
            self.assertEqual(d.group["name"], expected_group_name)
            
            expected_group_id = grp.getgrnam(GROUP).gr_gid
            self.assertEqual(d.group["id"], expected_group_id)
            
            expected_group_members = grp.getgrnam(GROUP).gr_mem
            self.assertSequenceEqual(d.group["members"], expected_group_members)            
        
        return   
    
    @unittest.skipUnless(IS_UNIX_LIKE_ROOT_USER, "Test requires running as root")
    def test_change_owner_of_directory(self):
        td = tempfile.TemporaryDirectory()
        with TemporaryDirectoryHandler(td):
            d = Directory(td.name)
            
            ORIGINAL_OWNER_NAME = d.owner["username"]
            ORIGINAL_OWNER_ID = d.owner["user_id"]
            ORIGINAL_GROUP_NAME = d.group["name"]
            ORIGINAL_GROUP_ID = d.group["id"]
            
            all_users_by_id = [u.pw_uid for u in pwd.getpwall()]
            all_users_by_name = [u.pw_name for u in pwd.getpwall()]
            
            # Change the Owner via ID
            if all_users_by_id[0] == ORIGINAL_OWNER_ID:
                new_owner_id = all_users_by_id[1]
            else:
                new_owner_id = all_users_by_id[0]
                
            d.change_owner(new_owner_id)
            self.assertEqual(
                d.owner["user_id"], new_owner_id, 
                msg="Change the owner, via user ID, assert failed"
            )
            self.assertEqual(
                d.group["id"], ORIGINAL_GROUP_ID, 
                msg=(
                    "When changing the owner, via user ID, the group was "
                    "changed as well."
                )
            )          
    
            # Change the Owner via Username
            if all_users_by_name[0] == ORIGINAL_OWNER_ID:
                new_owner_name = all_users_by_name[1]
            else:
                new_owner_name = all_users_by_name[0]
                
            d.change_owner(new_owner_name)
            self.assertEqual(
                d.owner["username"], new_owner_name, 
                msg="Change the owner, via username, assert failed"
            )
            self.assertEqual(
                d.group["name"], ORIGINAL_GROUP_NAME, 
                msg=(
                    "When changing the owner, via username, the group was "
                    "changed as well."
                )
            )         
        
        return    
    
    @unittest.skipUnless(IS_UNIX_LIKE_ROOT_USER, "Test requires running as root")
    def test_change_group_of_directory(self):
        td = tempfile.TemporaryDirectory()    
        with TemporaryDirectoryHandler(td):
            d = Directory(td.name)
            
            ORIGINAL_OWNER_NAME = d.owner["username"]
            ORIGINAL_OWNER_ID = d.owner["user_id"]
            ORIGINAL_GROUP_NAME = d.group["name"]
            ORIGINAL_GROUP_ID = d.group["id"]
            
            all_groups_by_id = [u.pw_uid for u in pwd.getpwall()]
            all_groups_by_name = [u.pw_name for u in pwd.getpwall()]
            
            # Change the Group via ID
            if all_groups_by_id[0] == ORIGINAL_GROUP_ID:
                new_group_id = all_groups_by_id[1]
            else:
                new_group_id = all_groups_by_id[0]
                
            d.change_group(new_group_id)
            self.assertEqual(
                d.group["id"], new_group_id, 
                msg="Change the group, via group ID, assert failed"
            )
            self.assertEqual(
                d.owner["user_id"], ORIGINAL_OWNER_ID, 
                msg=(
                    "When changing the group, via ID, the group was "
                    "changed as well."
                )
            )          
    
            # Change the Group via its Name
            if all_groups_by_name[0] == ORIGINAL_OWNER_ID:
                new_group_name = all_groups_by_name[1]
            else:
                new_group_name = all_groups_by_name[0]
                
            d.change_group(new_group_name)
            self.assertEqual(
                d.group["name"], new_group_name, 
                msg="Change the group, via name, assert failed"
            )
            self.assertEqual(
                d.owner["username"], ORIGINAL_OWNER_NAME, 
                msg=(
                    "When changing the group, via name, the owner was "
                    "changed as well."
                )
            )                 
        return      
    
    
    
@unittest.skipUnless(OPERATING_SYSTEM == "windows", "Windows-only test")    
class TestDirectoryWindows(unittest.TestCase):
    """Contains the tests specifically for Windows"""
    def test_windows_raise_exception_for_owner(self):
        with tempfile.TemporaryDirectory() as td:
            d = Directory(td)
            with self.assertRaises(NotImplementedError):
                d.owner
        return
    
    def test_windows_raise_exception_for_group(self):
        with tempfile.TemporaryDirectory() as td:
            d = Directory(td)
            with self.assertRaises(NotImplementedError):
                d.group
        return  
    
    def test_windows_raise_exception_for_change_owner(self):
        with tempfile.TemporaryDirectory() as td:
            d = Directory(td)
            self.assertRaises(NotImplementedError, d.change_owner, 1)

        return  
    
    def test_windows_raise_exception_for_change_group(self):
        with tempfile.TemporaryDirectory() as td:
            d = Directory(td)
            self.assertRaises(NotImplementedError, d.change_group, 1)

        return     
    
    
# Custom Classes (non-tests)  
class TemporaryDirectoryHandler:
    """This class should only be used (as a context manager) by tests that 
    rename, move, or delete a temporary directory before the tempfile object's
    .cleanup method is called. It can also be used by any tests that, for
    whateve reason, can't or won't use the standard tempfile context manager."""
    def __init__(self, temporary_directory):
        """
        Construct the object
        
        Parameters:
        temporary_directory -- (tempfile object) needed so that its .close() 
                                method can be called on it.
        
        """
        self._temporary_directory = temporary_directory
        return
    
    def __enter__(self):
        # Nothing needs to happen here.
        pass
    
    def __exit__(self, *args):
        # Catch the FileNotFoundError on .cleanup() to avoid the calling test 
        # outputting that it ignored an exception when the temporary file was
        # garbage collected (i.e., when .__del__() is called).          
        try:
            self._temporary_directory.cleanup()
        except FileNotFoundError:
            # This is normal, since the file was closed.
            pass         
        
        return
    


if __name__ == "__main__":
    unittest.main()