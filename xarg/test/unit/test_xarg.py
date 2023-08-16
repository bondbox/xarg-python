import unittest

from xarg import xarg


class TestXarg(unittest.TestCase):

    def setUp(self):
        self.xarg = xarg("xarg")


if __name__ == "__main__":
    unittest.main()
