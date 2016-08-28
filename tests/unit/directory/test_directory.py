"""Contains the unit tests for the inner directory package"""

import unittest
import os

from classyfd import Directory

class TestDirectory(unittest.TestCase):
    def setUp(self):
        self.fake_path = os.path.abspath("hello-world-dir")
        return
    
    def test_create_directory_object(self):
        d = Directory(self.fake_path)
        self.assertTrue(d)
        return


if __name__ == "__main__":
    unittest.main()