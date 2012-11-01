import unittest
import os.path

from tests.test_integration import TestIntegration


class TestBranchesDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestBranchesDirIntegration(TestIntegration):

	def test_is_directory(self):
		branches_dir_path = self.make_branches_dir_path()
		
		self.assertTrue(os.path.isdir(branches_dir_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
