import unittest
import stat

from gitviewfs_objects import SymLink


class TestSymlink(unittest.TestCase):
	
	def test_is_symlink(self):
		class MockSymLink(SymLink):
			def get_target_object(self): pass
		symlink = MockSymLink(name='ignored')
		
		attrs = symlink._get_attrs()
		
		mode = attrs[stat.ST_MODE]
		self.assertTrue(stat.S_ISLNK(mode))
	
	def test_readlink_returns_path_of_target_object(self):
		PATH = '/xyz/abc'
		class TargetObject(object):
			def get_path(self):
				return PATH
		class MockSymLink(SymLink):
			def get_target_object(self):
				return TargetObject()
		symlink = MockSymLink(name='ignored')
		
		path = symlink.readlink()
		
		self.assertEqual(PATH, path)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
