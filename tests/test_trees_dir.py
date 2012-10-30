import unittest
import os

from tests.test_integration import TestIntegration


class TestTreesDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestTreesDirIntegration(TestIntegration):
	
	def test_trees_dir_is_directory(self):
		trees_dir_path = self.make_trees_dir_path()
		self.assertTrue(os.path.isdir(trees_dir_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
