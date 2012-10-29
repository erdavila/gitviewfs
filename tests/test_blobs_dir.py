import unittest

from gitviewfs_objects import BlobsDir, ObjectsDir, get_gitviewfs_object
import stat
from tests.test_integration import TestIntegration
import os


class TestBlobsDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_getattr_returns_directory_type(self):
		blobs_dir = BlobsDir(parent=None, name='name')
		
		attr = blobs_dir.getattr()
		
		self.assertTrue(stat.S_ISDIR(attr.st_mode))
	
	def get_path(self):
		blobs_dir = BlobsDir.INSTANCE
		
		path = blobs_dir.get_path()
		
		self.assertEqual('/objects/blobs', path)


class TestBlobsDirIntegration(TestIntegration):
	
	def test_blobs_dir_is_directory(self):
		blobs_path = os.path.join(self.mountpoint, ObjectsDir.NAME, BlobsDir.NAME)
		self.assertTrue(os.path.isdir(blobs_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
