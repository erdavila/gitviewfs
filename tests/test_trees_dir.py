import unittest
import os

from tests.test_integration import TestIntegration
from gitviewfs_objects import ObjectsDir, TreesDir


class TestTreesDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestTreesDirIntegration(TestIntegration):
	
	def test_trees_dir_is_directory(self):
		trees_dir = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME)
		self.assertTrue(os.path.isdir(trees_dir))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()