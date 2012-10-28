import unittest

from gitviewfs_objects import HeadSymLink, RefsDir
import stat
from tests.test_integration import TestIntegration
import os


class TestHeadSymLink(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass


	def test_getattr_returns_symlink_type(self):
		head_symlink = HeadSymLink(parent=None)
		
		attr = head_symlink.getattr()
		
		self.assertTrue(stat.S_ISLNK(attr.st_mode))


class TestHeadSymLinkIntegration(TestIntegration):
	
	def test_HEAD_is_symlink(self):
		head_ref = os.path.join(self.mountpoint, RefsDir.NAME, 'HEAD')
		self.assertTrue(os.path.islink(head_ref))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
