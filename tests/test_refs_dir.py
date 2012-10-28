import unittest

from gitviewfs_objects import RefsDir
from tests.test_integration import TestIntegration
import os


class TestRefsDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_list_refs_dir(self):
		refs_dir = RefsDir(None)
		items = refs_dir.list()
		self.assertItemsEqual(['HEAD', 'branches', 'tags', 'remotes'], items)


class TestRefsDirIntegration(TestIntegration):
	
	def test_list_refs_dir(self):
		refs_dir = os.path.join(self.mountpoint, RefsDir.NAME)
		items = os.listdir(refs_dir)
		self.assertItemsEqual(['HEAD', 'branches', 'tags', 'remotes'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
