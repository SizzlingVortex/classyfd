"""Contains the unit tests for the inner file package"""

import unittest
import tempfile
import os
import pathlib
import shutil
import platform
import io
# Unix-like Only Imports
try:
    import pwd
    import grp
except ImportError:
    pass

from classyfd import File, FileError, InvalidFileValueError, utils, config


# Globals
OPERATING_SYSTEM = platform.system().lower()
IS_OS_POSIX_COMPLIANT = utils.determine_if_os_is_posix_compliant()

IS_UNIX_LIKE_ROOT_USER = None
if IS_OS_POSIX_COMPLIANT:
    # Determine if the User Running Python is "root" or not
    IS_UNIX_LIKE_ROOT_USER = utils.determine_if_running_as_root_user()
    

# Tests
class TestFile(unittest.TestCase):
    """Contains the cross-platform tests"""
    def setUp(self):
        self.fake_path = os.path.abspath("hello-world.txt")
        return
    
    def test_create_file_object(self):
        f = File(self.fake_path)
        self.assertTrue(f)
        return
    
    def test_raise_exception_for_empty_str_path_when_creating_file_object(self):
        self.assertRaises(InvalidFileValueError, File, "")
        return
    
    def test_raise_exception_when_path_is_an_existing_directory(self):
        self.assertRaises(IsADirectoryError, File, os.getcwd())
        return
    
    def test_repr(self):
        """Test the official string representation of an instance"""
        f = File(self.fake_path)
        expected_repr = (
            '{class_name}("{path}")'
            .format(class_name=File.__name__, path=f.path)
        )
        self.assertEqual(repr(f), expected_repr)
        return
    
    def test_str(self):
        """Test the informal string representation of an instance"""
        self.fake_path = os.path.abspath("hello-world.txt")
        f = File(self.fake_path)
        self.assertEqual(str(f), self.fake_path)
        return    
    
    def test_file_exists(self):
        # The File Will not Exist
        f = File(self.fake_path)
        self.assertFalse(f.exists, msg="The file should not exist")
        
        # The File Will Exist
        with tempfile.NamedTemporaryFile() as tf:
            f = File(tf.name)
            self.assertTrue(f.exists, msg="The file should exist")
        
        return
    
    def test_get_path(self):
        """
        A normalized, absolute path should be returned -- even if a relative
        path is originally given when the instance object is created.
        
        """
        # Pass an Absolute Path
        f = File(self.fake_path)
        self.assertEqual(
            f.path, self.fake_path, msg="The absolute paths were not equal"
        )
            
        # Pass Relative Paths
        #
        # Assign fake file paths
        relative_paths = ["./hello-world.txt", "../goodbye-world.txt"]
        absolute_paths = [os.path.abspath(p) for p in relative_paths]
        for i, path in enumerate(relative_paths):
            f = File(path)
            with self.subTest(path=path):
                self.assertEqual(
                    f.path, absolute_paths[i]
                )
                
        # Pass a Relative, Non-Normalized Path
        non_normalized_path = "directory1\\directory2\\hello-world.txt"
        expected_path = utils.normalize_path(
            os.path.abspath(non_normalized_path)
        )
        
        f = File(non_normalized_path)
        self.assertEqual(
            f.path, expected_path, 
            msg="The relative, non-normalized path assert failed"
        )        
        
        return
    
    def test_set_path(self):
        """
        Setting a path should always store its absolute path, even if a 
        relevant path is given."""
        # Absolute Path Given
        f = File(self.fake_path)
        # Reassign the same path
        f.path = self.fake_path
        self.assertEqual(
            f.path, self.fake_path, msg="The absolute path assert failed"
        )
        
        # Relative Path Given
        #
        # Change the path to just the file's name
        f.path = f.name
        self.assertEqual(
            f.path, self.fake_path, msg="The relative path assert failed"
        )
        
        # Pass a Relative, Non-Normalized Path
        non_normalized_path = "directory1\\directory2\\hello-world.txt"
        expected_path = utils.normalize_path(
            os.path.abspath(non_normalized_path)
        )
        
        f = File(self.fake_path)
        f.path = non_normalized_path
        
        self.assertEqual(
            f.path, expected_path, 
            msg="The relative, non-normalized path assert failed"
        )          
        
        return
    
    def test_raise_exception_for_setting_path_to_a_directory(self):
        with tempfile.TemporaryDirectory() as td:
            f = File(self.fake_path)
            try:
                f.path = td
            except IsADirectoryError:
                # Do nothing, as this is the right exception to be raised
                pass
            else:
                self.fail("An IsADirectoryError should have been raised")
        
        return
    
    def test_get_name(self):
        """
        Should get the final part of the file's path (including any extensions)
        
        """
        fake_paths = (
            # With extension
            "./hello-world.txt", 
            # Without extension
            "./hello-world"
        )
        
        for p in fake_paths:
            with self.subTest(path=p):
                f = File(p)            
                expected_file_name = pathlib.Path(f.path).name
                self.assertEqual(f.name, expected_file_name)
        
        return
    
    def test_get_parent_directory_path(self):
        # One level up
        fake_path = "/home/someuserthatdoesntexist/Documents/hello-world.txt"
        f = File(fake_path)
        expected_parent = os.path.abspath(
            "/home/someuserthatdoesntexist/Documents"
        )
        
        self.assertEqual(
            f.parent, expected_parent, msg="One level up assert failed"
        )
        
        # Zero should be treated the same as one level up
        expected_parent = os.path.abspath(
            "/home/someuserthatdoesntexist/Documents"
        )
        
        self.assertEqual(
            f.get_parent(levels=0), expected_parent,
            msg="Zero should be treated the same as one level up"
        )          
        
        # Three levels up
        expected_parent = os.path.abspath("/home")
        self.assertEqual(
            f.get_parent(levels=3), expected_parent,
            msg="Three levels up assert failed"
        )      
        
        return
    
    def test_raise_exception_for_get_parent_with_negative_values(self):
        f = File(self.fake_path)
        self.assertRaises(InvalidFileValueError, f.get_parent, levels=-1)
        return
    
    def test_get_size(self):
        # Standard ASCII Characters Only
        data = "Hello, world!"
        # In this case, each character is just one byte.
        expected_size = len(data)
        with tempfile.NamedTemporaryFile(mode="w") as tf:
            tf.write(data)
            
            # Write to the file immediately since the file's size is needed
            tf.flush()
            os.fsync(tf.fileno())

            f = File(tf.name)
            self.assertEqual(
                f.size, expected_size, 
                msg="The standard ASCII characters assert failed"
            )
            
        # Uncommon Unicode Characters
        #
        data = "ÅBÇÐËFG"
        # Due to the unicode characters used, the file should be 11 bytes --
        # as previously, and manually, testing showed these results.
        expected_size = 11
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as tf:
            tf.write(data)
            
            # Write to the file immediately since the file's size is needed
            tf.flush()
            os.fsync(tf.fileno())
            
            f = File(tf.name)
            self.assertEqual(
                f.size, expected_size,
                msg="Uncommon unicode characters assert failed"
            )        
        
        return
    
    def test_get_stem(self):
        """Should get the file's name, excluding its extension"""
        # No Extensions in Given Path
        fake_path = pathlib.Path(self.fake_path).stem
        expected_stem = fake_path
        f = File(fake_path)
        self.assertEqual(
            f.stem, expected_stem, msg="No extension assert failed"
        )
        
        # One Extension in Given Path
        f = File(self.fake_path)
        expected_stem = pathlib.Path(f.path).stem
        self.assertEqual(
            f.stem, expected_stem, msg="One extension assert failed"
        )
        
        # Multiple Extensions in Given Path
        fake_path = "backup.tar.gz"
        # The final extension will be removed
        expected_stem = pathlib.Path(fake_path).stem
        f = File(fake_path)
        self.assertEqual(
            f.stem, expected_stem, msg="Multiple extensions assert failed"
        )        
        
        return
    
    def test_get_extension(self):
        # No Extensions in Given Path
        #
        # Remove the extension from the fake file
        fake_path = pathlib.Path(self.fake_path).stem
        f = File(fake_path)        
        expected_extension = ""
        self.assertEqual(
            f.extension, expected_extension, msg="No extension assert failed"
        )
        
        # One Extension in Given Path
        f = File(self.fake_path)
        expected_extension = ".txt"
        self.assertEqual(
            f.extension, expected_extension, msg="One extension assert failed"
        )
        
        # Multiple Extensions in Given Path 
        fake_path = "backup.tar.gz"
        expected_extension = ".gz"
        f = File(fake_path)
        self.assertEqual(
            f.extension, expected_extension, 
            msg="Multiple extensions assert failed"
        )           
        
        return
    
    def test_get_all_extensions(self):
        # No Extensions in Given Path
        #
        # Remove the extension from the fake file
        fake_path = pathlib.Path(self.fake_path).stem
        f = File(fake_path)        
        expected_extension = []
        self.assertEqual(
            f.extensions, expected_extension, msg="No extension assert failed"
        )
        
        # One Extension in Given Path
        f = File(self.fake_path)
        expected_extension = [".txt"]
        self.assertEqual(
            f.extensions, expected_extension, msg="One extension assert failed"
        )
        
        # Multiple Extensions in Given Path 
        fake_path = "backup.tar.gz"
        expected_extension = [".tar", ".gz"]
        f = File(fake_path)
        self.assertEqual(
            f.extensions, expected_extension, 
            msg="Multiple extensions assert failed"
        )         
        
        return
    
    def test_remove_file(self):
        tf = tempfile.NamedTemporaryFile()
        with TemporaryFileHandler(tf):
            f = File(tf.name)
            f.remove()
            self.assertFalse(os.path.exists(tf.name))
        return
    
    def test_rename_file(self):
        tf = tempfile.NamedTemporaryFile()
        with TemporaryFileHandler(tf):
            # The base directory will be the same for both the original and 
            # renamed file.
            BASE_DIRECTORY = str(pathlib.Path(tf.name).parent)
            
            # Rename the File
            renamed_file_name = utils.get_random_file_name(BASE_DIRECTORY)
            expected_new_file_path = os.path.join(BASE_DIRECTORY, 
                                                  renamed_file_name)
            
            # Check if the file already exists. It should only exist if this 
            # file's tests were run previously. In such a case, it is fine to
            # just delete the file.
            if os.path.exists(expected_new_file_path):
                os.remove(expected_new_file_path)
            
            self.assertFalse(
                os.path.exists(expected_new_file_path), 
                msg="The file can't be renamed because the path already exists"
            )
            
            f = File(tf.name)
            f.rename(renamed_file_name)
            self.assertTrue(
                os.path.exists(expected_new_file_path), 
                msg="The file was not renamed"
            )
            
        return
    
    def test_raise_exception_for_rename_with_path(self):
        """
        An exception should be raised when a path (instead of just a new file
        name) is given. This is likely to occur if a user thinks rename is just
        like GNU mv -- in which mv actually accepts paths.
        
        """
        tf = tempfile.NamedTemporaryFile()
        BASE_DIRECTORY = str(pathlib.Path(tf.name).parent)
        
        # Try to Rename the File
        renamed_file_name = utils.get_random_file_name(BASE_DIRECTORY)
        new_file_path = os.path.join(BASE_DIRECTORY, renamed_file_name)
        f = File(tf.name)
        self.assertRaises(InvalidFileValueError, f.rename, new_file_path)
        
        return
    
    def test_rename_updates_path(self):
        """If a file object is renamed, then its path should be updated"""
        tf = tempfile.NamedTemporaryFile()
        with TemporaryFileHandler(tf):
            BASE_DIRECTORY = str(pathlib.Path(tf.name).parent)
            
            f = File(tf.name)
            new_file_name = utils.get_random_file_name(BASE_DIRECTORY)
            expected_path = os.path.join(BASE_DIRECTORY, new_file_name)            
            
            try:
                f.rename(new_file_name)
                self.assertEqual(f.path, expected_path)
            finally:
                # Delete the newly renamed file so that future test runs don't
                # raise a FileExistsError.
                os.remove(expected_path)
                
        return
    
    def test_raise_exception_on_rename_to_existing_path(self):
        """If a file is renamed to a file whose path already exists, then an 
        exception should be raised."""
        # Create two temporary files
        tf1 = tempfile.NamedTemporaryFile()
        tf1_file_name = File(tf1.name).name
        tf2 = tempfile.NamedTemporaryFile()
        
        # Try to rename the second temporary file to that of the first
        with TemporaryFileHandler(tf1):
            with TemporaryFileHandler(tf2):
                f = File(tf2.name)
                self.assertRaises(FileExistsError, f.rename, tf1_file_name)
        
        return
    
    def test_replace_existing_file_on_rename(self):
        # The temporary files need to be closed, but not deleted when .close()
        # is called. Otherwise, Windows will raise a PermissionError.
        tf1 = tempfile.NamedTemporaryFile(delete=False)
        tf1_file_name = File(tf1.name).name
        tf2 = tempfile.NamedTemporaryFile(delete=False)
        
        tf1.close()
        tf2.close()
        
        # Try to rename the second temporary file to that of the first
        with TemporaryFileHandler(tf1):
            with TemporaryFileHandler(tf2):
                f = File(tf2.name)
                try:
                    f.rename(tf1_file_name, replace_existing_file=True)
                except FileExistsError:
                    self.fail(
                        "The file should have been replaced, but a "
                        "FileExistsError was raised instead."
                    )
                else:
                    self.assertFalse(os.path.exists(tf2.name))
                    self.assertTrue(os.path.exists(tf1.name))
        
        return
    
    def test_move_file(self):
        td1 = tempfile.TemporaryDirectory()
        td2 = tempfile.TemporaryDirectory()
        
        tf = tempfile.NamedTemporaryFile()
        f = File(tf.name)
        
        expected_moved_file_path = os.path.join(td2.name, f.name)        
        self.assertFalse(os.path.exists(expected_moved_file_path))
        
        with TemporaryDirectoryHandler(td1):
            with TemporaryDirectoryHandler(td2):
                with TemporaryFileHandler(tf):
                    f.move(td2.name)
                    self.assertTrue(os.path.exists(expected_moved_file_path))
                
        return
    
    def test_move_file_updates_path(self):
        """When a file is moved, its path should be updated."""
        td1 = tempfile.TemporaryDirectory()
        td2 = tempfile.TemporaryDirectory()
        
        tf = tempfile.NamedTemporaryFile()
        f = File(tf.name)
        
        with TemporaryDirectoryHandler(td1):
            with TemporaryDirectoryHandler(td2):
                with TemporaryFileHandler(tf):
                    expected_moved_file_path = os.path.join(td2.name, f.name)
                    f.move(td2.name)
                    self.assertEqual(f.path, expected_moved_file_path)
                
        return
    
    def test_move_file_with_new_file_name(self):
        td1 = tempfile.TemporaryDirectory()
        td2 = tempfile.TemporaryDirectory()
        
        tf = tempfile.NamedTemporaryFile()
        f = File(tf.name)
        
        new_file_name = "hello-world.txt"
        expected_moved_file_path = os.path.join(td2.name, new_file_name)        
        self.assertFalse(os.path.exists(expected_moved_file_path))
        
        with TemporaryDirectoryHandler(td1):
            with TemporaryDirectoryHandler(td2):
                with TemporaryFileHandler(tf):
                    f.move(td2.name, new_file_name=new_file_name)
                    self.assertTrue(os.path.exists(expected_moved_file_path))
                
        return
    
    def test_raise_exception_for_move_with_file_name_path(self):
        """If a path is used as the file name during a move operation, then an
        exception should be raised."""
        td1 = tempfile.TemporaryDirectory()
        td2 = tempfile.TemporaryDirectory()
        
        tf = tempfile.NamedTemporaryFile()
        f = File(tf.name)
        
        new_file_name = "./hello-world.txt"
        
        with TemporaryFileHandler(tf):
            try:
                self.assertRaises(
                    InvalidFileValueError, f.move, td2.name, 
                    new_file_name=new_file_name
                )                
            finally:
                td1.cleanup()
                td2.cleanup()        
        
        return
    
    def test_raise_exception_on_move_to_existing_path(self):
        tf1 = tempfile.NamedTemporaryFile()
        tf2 = tempfile.NamedTemporaryFile()
        
        f1 = File(tf1.name)
        f2 = File(tf2.name)
              
        with TemporaryFileHandler(tf1):
            with TemporaryFileHandler(tf2):
                self.assertRaises(
                    FileExistsError, f1.move, f2.parent, new_file_name=f2.name
                )
            
        
        return
    
    def test_replace_existing_file_on_move(self):
        # The temporary files need to be closed, but not deleted when .close()
        # is called. Otherwise, Windows will raise a PermissionError.
        tf1 = tempfile.NamedTemporaryFile(delete=False)
        tf2 = tempfile.NamedTemporaryFile(delete=False)
        
        tf1.close()
        tf2.close()
        
        f1 = File(tf1.name)
        f2 = File(tf2.name)
        
        # Try to replace the second temporary file with the first one
        with TemporaryFileHandler(tf1):
            with TemporaryFileHandler(tf2):
                try:
                    f1.move(
                        f2.parent, new_file_name=f2.name, 
                        replace_existing_file=True
                    )
                except FileExistsError:
                    self.fail(
                        "The file should have been replaced, but a "
                        "FileExistsError was raised instead."
                    )
                else:
                    self.assertFalse(os.path.exists(tf1.name))
                    self.assertTrue(os.path.exists(tf2.name))
        
        return
    
    def test_is_file(self):
        # Fake Path
        f = File(self.fake_path)
        self.assertFalse(f.is_file, msg="The fake path assert failed")
        
        # A Real File
        with tempfile.NamedTemporaryFile() as tf:
            f = File(tf.name)
            self.assertTrue(f.is_file, msg="Real file assert failed")
        
        # The File No Longer Exists
        with tempfile.NamedTemporaryFile() as tf:
            f = File(tf.name)
        self.assertFalse(f.is_file, msg="File no longer exists assert failed")
            
        # File Path that Turned into a Directory Path
        #
        # First, create the file
        with tempfile.NamedTemporaryFile() as tf:
            tf_path = tf.name
            f = File(tf.name)
        self.assertFalse(f.is_file)
        # Now create the directory using the same path the file had
        os.mkdir(tf_path)
        self.assertFalse(
            f.is_file, 
            msg="File path turned directory path assert failed"
        )
        self.assertTrue(
            os.path.isdir(tf_path),
            msg="File path turned directory path assert failed"
        )
        
        return
    
    def test_open_returns_file_object(self):
        
        # Text File Object
        with tempfile.NamedTemporaryFile(mode="w", encoding=config._ENCODING) as tf:
            my_file = File(tf.name) 
            # Non-context manager
            f = my_file.open()
            try:
                self.assertIsInstance(
                    f, io.TextIOBase, 
                    msg="The text file, non-context manager, assert failed"
                )
            except Exception:
                # Included only to follow the syntax rules
                raise
            else:
                f.close()
            
            # Context manager
            with my_file.open() as f:
                pass
            self.assertIsInstance(
                f, io.TextIOBase, 
                msg="The text file, context manager, assert failed"
            )            
                
        # Binary File Object
        with tempfile.NamedTemporaryFile(mode="wb") as tf:
            my_file = File(tf.name) 
            # Non-context manager
            f = my_file.open(mode="wb")
            try:
                self.assertIsInstance(
                    f, (io.BufferedIOBase, io.RawIOBase), 
                    msg="The binary file, non-context manager, assert failed"
                )
            except Exception:
                # Included only to follow the syntax rules
                raise
            else:
                f.close()
            
            # Context manager
            with my_file.open(mode="wb") as f:
                self.assertIsInstance(
                    f, (io.BufferedIOBase, io.RawIOBase), 
                    msg="The binary file, context manager, assert failed"
                )                
        
        return
    

@unittest.skipUnless(IS_OS_POSIX_COMPLIANT, "Unix-like only test")
class TestFileUnixLike(unittest.TestCase):
    """Containst the tests specifically for Unix-like operating systems"""
    def test_get_owner_of_file(self):
        
        with tempfile.NamedTemporaryFile(mode="w") as tf:
            f = File(tf.name)
            OWNER = pathlib.Path(f.path).owner()
            
            expected_owner_username = pwd.getpwnam(OWNER).pw_name
            self.assertEqual(
                f.owner["username"], expected_owner_username, 
                msg="The owner usernames are not equal"
            )
            
            expected_owner_user_id = pwd.getpwnam(OWNER).pw_uid
            self.assertEqual(
                f.owner["user_id"], expected_owner_user_id, 
                msg="The owner IDs are not equal"
            )
            
            expected_owner_group_id = pwd.getpwnam(OWNER).pw_gid
            self.assertEqual(
                f.owner["group_id"], expected_owner_group_id, 
                msg="The group IDs are not equal"
            )
            
            expected_owner_directory = pwd.getpwnam(OWNER).pw_dir
            self.assertEqual(
                f.owner["directory"], expected_owner_directory, 
                msg="The directories are not equal"
            )            
        
        return
    
    def test_get_group_of_file(self):
        with tempfile.NamedTemporaryFile(mode="w") as tf:
            f = File(tf.name)
            GROUP = pathlib.Path(f.path).group()
            
            expected_group_name = grp.getgrnam(GROUP).gr_name
            self.assertEqual(f.group["name"], expected_group_name)
            
            expected_group_id = grp.getgrnam(GROUP).gr_gid
            self.assertEqual(f.group["id"], expected_group_id)
            
            expected_group_members = grp.getgrnam(GROUP).gr_mem
            self.assertSequenceEqual(f.group["members"], expected_group_members)            
        
        return        
    
    @unittest.skipUnless(IS_UNIX_LIKE_ROOT_USER, "Test requires running as root")
    def test_change_owner_of_file(self):
        # Keep the temp file upon closing it
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.close()
        
        with TemporaryFileHandler(tf):
            f = File(tf.name)
            
            ORIGINAL_OWNER_NAME = f.owner["username"]
            ORIGINAL_OWNER_ID = f.owner["user_id"]
            ORIGINAL_GROUP_NAME = f.group["name"]
            ORIGINAL_GROUP_ID = f.group["id"]
            
            all_users_by_id = [u.pw_uid for u in pwd.getpwall()]
            all_users_by_name = [u.pw_name for u in pwd.getpwall()]
            
            # Change the Owner via ID
            if all_users_by_id[0] == ORIGINAL_OWNER_ID:
                new_owner_id = all_users_by_id[1]
            else:
                new_owner_id = all_users_by_id[0]
                
            f.change_owner(new_owner_id)
            self.assertEqual(
                f.owner["user_id"], new_owner_id, 
                msg="Change the owner, via user ID, assert failed"
            )
            self.assertEqual(
                f.group["id"], ORIGINAL_GROUP_ID, 
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
                
            f.change_owner(new_owner_name)
            self.assertEqual(
                f.owner["username"], new_owner_name, 
                msg="Change the owner, via username, assert failed"
            )
            self.assertEqual(
                f.group["name"], ORIGINAL_GROUP_NAME, 
                msg=(
                    "When changing the owner, via username, the group was "
                    "changed as well."
                )
            )         
        
        return

    @unittest.skipUnless(IS_UNIX_LIKE_ROOT_USER, "Test requires running as root")
    def test_change_group_of_file(self):
        # Keep the temp file upon closing it
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.close()
        
        with TemporaryFileHandler(tf):
            f = File(tf.name)
            
            ORIGINAL_OWNER_NAME = f.owner["username"]
            ORIGINAL_OWNER_ID = f.owner["user_id"]
            ORIGINAL_GROUP_NAME = f.group["name"]
            ORIGINAL_GROUP_ID = f.group["id"]
            
            all_groups_by_id = [u.pw_uid for u in pwd.getpwall()]
            all_groups_by_name = [u.pw_name for u in pwd.getpwall()]
            
            # Change the Group via ID
            if all_groups_by_id[0] == ORIGINAL_GROUP_ID:
                new_group_id = all_groups_by_id[1]
            else:
                new_group_id = all_groups_by_id[0]
                
            f.change_group(new_group_id)
            self.assertEqual(
                f.group["id"], new_group_id, 
                msg="Change the group, via group ID, assert failed"
            )
            self.assertEqual(
                f.owner["user_id"], ORIGINAL_OWNER_ID, 
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
                
            f.change_group(new_group_name)
            self.assertEqual(
                f.group["name"], new_group_name, 
                msg="Change the group, via name, assert failed"
            )
            self.assertEqual(
                f.owner["username"], ORIGINAL_GROUP_NAME, 
                msg=(
                    "When changing the group, via name, the owner was "
                    "changed as well."
                )
            )                 
        return    
        

@unittest.skipUnless(OPERATING_SYSTEM == "windows", "Windows-only test")    
class TestFileWindows(unittest.TestCase):
    """Contains the tests specifically for Windows"""
    def test_windows_raise_exception_for_owner(self):
        with tempfile.NamedTemporaryFile() as tf:
            f = File(tf.name)
            with self.assertRaises(NotImplementedError):
                f.owner
        return
    
    def test_windows_raise_exception_for_group(self):
        with tempfile.NamedTemporaryFile() as tf:
            f = File(tf.name)
            with self.assertRaises(NotImplementedError):
                f.group
        return        
    
    def test_windows_raise_exception_for_change_owner(self):
        with tempfile.NamedTemporaryFile() as tf:
            f = File(tf.name)
            self.assertRaises(NotImplementedError, f.change_owner, 1)

        return
    
    def test_windows_raise_exception_for_change_group(self):
        with tempfile.NamedTemporaryFile() as tf:
            f = File(tf.name)
            self.assertRaises(NotImplementedError, f.change_group, 1)

        return     
    
    
# Custom Classes
class TemporaryFileHandler:
    """This class should only be used (as a context manager) by tests that 
    rename, move, or delete a real temporary file before the tempfile object's
    .close method is called. It can also be used by any tests that, for
    whateve reason, can't or won't use the standard tempfile context manager."""
    def __init__(self, temporary_file):
        """
        Construct the object
        
        Parameters:
        temporary_file -- (tempfile object) needed so that its .close() method
                          can be called on it.
        
        """
        self._temporary_file = temporary_file
        return
    
    def __enter__(self):
        # Nothing needs to happen here.
        pass
    
    def __exit__(self, *args):
        # Catch the FileNotFoundError on .close() to avoid the calling test 
        # outputting that it ignored an exception when the temporary file was
        # garbage collected (i.e., when .__del__() is called).          
        try:
            self._temporary_file.close()
        except FileNotFoundError:
            # This is normal, since the file was closed.
            pass         
        
        return
    
class TemporaryDirectoryHandler:
    def __init__(self, temporary_directory):
        """
        Construct the object
        
        Parameters:
        temporary_directory -- (tempfile.TemporaryDirectory object) needed
                               so that its .cleanup() method can be called.
        
        """
        self._temporary_directory = temporary_directory
        return    
    
    def __enter__(self):
        # Nothing needs to happen here.
        pass    
    
    def __exit__(self, *args):        
        try:
            self._temporary_directory.cleanup()
        except PermissionError:
            # Likely being raised because "the directory is not empty." This
            # exception was only ever raised on Windows, however.
            shutil.rmtree(self._temporary_directory.name)
        
        return 
    

if __name__ == "__main__":
    unittest.main()