"""Contains the unit tests for the inner directory package"""

import unittest

from classyfd import Directory

class TestDirectory(unittest.TestCase):
    def setUp(self):
        self.fake_path = os.path.abspath("hello-world-dir")
        return


if __name__ == "__main__":
    unittest.main()