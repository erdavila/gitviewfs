import unittest
import os.path
import subprocess

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
	
	def test_list(self):
		self.create_and_commit_file('some content')
		self.create_and_commit_file('Another cOnTeNt')
		
		CREATED_BRANCH = 'another-branch'
		subprocess.check_output(['git', 'checkout', '-b', CREATED_BRANCH, 'HEAD~1'])
		self.create_and_commit_file('YET another CoNtEnT')
		
		branches_dir_path = self.make_branches_dir_path()
		branches = os.listdir(branches_dir_path)
		
		self.assertItemsEqual(['master', CREATED_BRANCH], branches)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
