import unittest

from gitviewfs_objects import BlobsDir
import stat


class TestBlobsDir(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass


	def test_getattr_returns_directory_type(self):
		blobs_dir = BlobsDir(parent=None, name='name')
		
		attr = blobs_dir.getattr()
		
		self.assertTrue(stat.S_ISDIR(attr.st_mode))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
