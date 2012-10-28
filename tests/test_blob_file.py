import unittest

from gitviewfs_objects import BlobFile
import stat


class TestBlobFile(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass


	def test_getattr_returns_file_type(self):
		blob_file = BlobFile(parent=None, name='name')
		
		attr = blob_file.getattr()
		
		self.assertTrue(stat.S_ISREG(attr.st_mode))

	def test_getattr_returns_not_executable(self):
		blob_file = BlobFile(parent=None, name='name')
		
		attr = blob_file.getattr()
		
		self.assertFalse(attr.st_mode & stat.S_IXUSR)
		self.assertFalse(attr.st_mode & stat.S_IXGRP)
		self.assertFalse(attr.st_mode & stat.S_IXOTH)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
