import unittest

from fs_objects import HeadSymLink
import stat
import posix
import itertools


class TestHeadSymLink(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass


	def test_getattr_calls_parent_and_return_symlink_type(self):
		class Parent(object):
			getattr_called = False
			def getattr(self):
				self.getattr_called = True
				return posix.stat_result(itertools.repeat(0, 10))
		
		parent = Parent()
		head_symlink = HeadSymLink(parent=parent)
		attr = head_symlink.getattr()
		
		self.assertTrue(parent.getattr_called)
		self.assertTrue(stat.S_ISLNK(attr.st_mode))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
