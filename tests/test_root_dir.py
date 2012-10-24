import unittest

from dirs import RootDir


class Test(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_list_root_dir(self):
		dir = RootDir()
		items = dir.list()
		self.assertItemsEqual(['refs', 'objects', 'remotes'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
