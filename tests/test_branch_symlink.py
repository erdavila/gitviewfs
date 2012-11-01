import unittest
import subprocess

from tests.test_integration import TestIntegration


class TestBranchSymLink(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestBranchSymLinkIntegration(TestIntegration):

	def test_symlink(self):
		BRANCH = 'master'
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', BRANCH]).strip()
		branch_symlink_path = self.make_branch_symlink_path(BRANCH)
		
		self.assertSymLink(self.make_commit_dir_path(commit_sha1), branch_symlink_path)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
