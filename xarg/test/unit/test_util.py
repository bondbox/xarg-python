# coding:utf-8

import os
import unittest

from xarg import chdir


class test_chdir(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_chdir(self):
        self.assertRaises(AssertionError, chdir().popd)
        chdir().pushd(os.path.join("xarg", "test"))
        chdir().pushd("unit")
        chdir().popd()
        chdir().popd()
        self.assertRaises(AssertionError, chdir().popd)


if __name__ == "__main__":
    unittest.main()
