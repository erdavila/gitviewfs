import unittest

from gitviewfs_objects import get_gitviewfs_object
from tests import paths
import stat


class Test(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_getattr(self):
		commit_message_file = get_gitviewfs_object(paths.COMMIT_MESSAGE_FILE)
		CONTENT_SIZE = 142857
		def _get_content_size():
			return CONTENT_SIZE
		commit_message_file._get_content_size = _get_content_size
		
		attrs = commit_message_file.getattr()
		
		self.assertTrue(stat.S_ISREG(attrs.st_mode))
		
		self.assertFalse(attrs.st_mode & stat.S_IXUSR)
		self.assertFalse(attrs.st_mode & stat.S_IXGRP)
		self.assertFalse(attrs.st_mode & stat.S_IXOTH)
		
		self.assertEqual(CONTENT_SIZE, attrs.st_size)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_']
	unittest.main()