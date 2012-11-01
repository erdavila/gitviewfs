import unittest
import os.path

from tests.test_integration import TestIntegration


class TestCommitsDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestCommitsDirIntegration(TestIntegration):

	def test_is_directory(self):
		commits_dir_path = self.make_commits_dir_path()
		
		self.assertTrue(os.path.isdir(commits_dir_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_is_directory']
	unittest.main()