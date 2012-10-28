import unittest

from gitviewfs_objects import RefsDir


class TestRefsDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_list_refs_dir(self):
		refs_dir = RefsDir(None, RefsDir.NAME)
		items = refs_dir.list()
		self.assertItemsEqual(['HEAD', 'branches', 'tags', 'remotes'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
