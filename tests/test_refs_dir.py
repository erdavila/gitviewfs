import unittest

from fs_objects import RefsDir


class Test(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_list_refs_dir(self):
		dir = RefsDir(None, RefsDir.NAME)
		items = dir.list()
		self.assertItemsEqual(['HEAD', 'branches', 'tags', 'remotes'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
