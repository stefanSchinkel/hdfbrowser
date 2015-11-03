import sys
from os import path


# add module path
cwd = path.dirname( path.dirname( path.abspath(__file__) ) )
sys.path.append( cwd )
testFile = path.join(cwd,'sample/sample.hd5')
print testFile

from model.treeModel import TreeModel
from model.HDFModel import HDFModel
import unittest


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.tm = TreeModel();
        self.hdf = HDFModel(fileName=testFile);

    # basic world is round check
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def testModelNames(self):
        self.assertEqual(str(self.tm), 'TreeModel')
        self.assertEqual(str(self.hdf), 'HDFModel')

    def testFileName(self):
        self.assertEqual(str(self.hdf.fileName), testFile)

if __name__ == '__main__':
    unittest.main()

