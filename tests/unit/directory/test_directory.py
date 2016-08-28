"""Contains the unit tests for the inner directory package"""

import unittest


class TestDirectory(unittest.TestCase):
    def setUp(self):
        self.fake_path = os.path.abspath("hello-world-dir")
        return    


if __name__ == "__main__":
    unittest.main()