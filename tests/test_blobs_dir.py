import unittest
import stat
import os

from gitviewfs_objects import BlobsDir
from tests.test_integration import TestIntegration


class TestBlobsDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_get_stat_returns_directory_type(self):
		blobs_dir = BlobsDir.INSTANCE
		
		st = blobs_dir.get_stat()
		
		self.assertTrue(stat.S_ISDIR(st.st_mode))


class TestBlobsDirIntegration(TestIntegration):
	
	def test_is_directory(self):
		blobs_path = self.make_blobs_dir_path()
		self.assertTrue(os.path.isdir(blobs_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
