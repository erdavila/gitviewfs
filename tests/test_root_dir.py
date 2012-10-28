import unittest

from gitviewfs_objects import RootDir


class TestRootDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_list_root_dir(self):
		root_dir = RootDir()
		items = root_dir.list()
		self.assertItemsEqual(['refs', 'objects', 'remotes'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
