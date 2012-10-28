import unittest
import os

from gitviewfs_objects import root_dir
from tests.test_integration import TestIntegration


class TestRootDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_list_root_dir(self):
		items = root_dir.list()
		self.assertItemsEqual(['refs', 'objects', 'remotes'], items)


class TestRootDirIntegration(TestIntegration):
	
	def test_list_root_dir(self):
		items = os.listdir(self.mountpoint)
		self.assertItemsEqual(['refs', 'objects', 'remotes'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
