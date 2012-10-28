import unittest

from gitviewfs_objects import HeadSymLink
import stat


class TestHeadSymLink(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass


	def test_getattr_returns_symlink_type(self):
		head_symlink = HeadSymLink(parent=None)
		
		attr = head_symlink.getattr()
		
		self.assertTrue(stat.S_ISLNK(attr.st_mode))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
