# coding:utf-8

import os
from tempfile import TemporaryDirectory
import unittest

from xarg import chdir
from xarg import safile


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


class test_safile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text = "ZbbwpP4%oSwYxP=t+LkyXXzqL9fE8!"

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_backup_and_restore(self):
        with TemporaryDirectory() as thdl:
            path = os.path.join(thdl, "test")
            self.assertTrue(safile.backup(path))
            with open(path, "w") as whdl:
                whdl.write(self.text)
            self.assertTrue(safile.backup(path))
            self.assertRaises(AssertionError, safile.backup, path)
            with open(path, "w") as whdl:
                whdl.write("unittest")
            self.assertTrue(safile.restore(path))
            with open(path, "r") as rhdl:
                self.assertEqual(rhdl.read(), self.text)


if __name__ == "__main__":
    unittest.main()
