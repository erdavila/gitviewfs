import unittest
import os

from gitviewfs_objects import RefsDir
from tests.test_integration import TestIntegration


class TestRefsDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_list(self):
		refs_dir = RefsDir.INSTANCE
		items = refs_dir.list()
		self.assertItemsEqual(['HEAD', 'branches', 'tags', 'remotes'], items)


class TestRefsDirIntegration(TestIntegration):
	
	def test_list(self):
		refs_dir_path = self.make_refs_dir_path()
		items = os.listdir(refs_dir_path)
		self.assertItemsEqual(['HEAD', 'branches', 'tags', 'remotes'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
