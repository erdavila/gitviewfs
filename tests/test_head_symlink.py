import unittest
import stat
import os

from gitviewfs_objects import HeadSymLink
from tests.test_integration import TestIntegration


class TestHeadSymLink(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_getattr_returns_symlink_type(self):
		head_symlink = HeadSymLink.INSTANCE
		
		attr = head_symlink.getattr()
		
		self.assertTrue(stat.S_ISLNK(attr.st_mode))


class TestHeadSymLinkIntegration(TestIntegration):
	
	def test_is_symlink(self):
		head_symlink_path = self.make_head_symlink_path()
		self.assertTrue(os.path.islink(head_symlink_path))
	
	def test_link(self):
		self.create_and_commit_file()
		expected_absolute_path = self.make_branch_symlink_path('master')
		symlink_path = self.make_head_symlink_path()
		
		self.assertSymLink(expected_absolute_path, symlink_path)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
