import unittest
import os
import subprocess

from tests.test_integration import TestIntegration
from gitviewfs_objects import CommitsDir


class TestCommitDir(unittest.TestCase):
	
	def test_list(self):
		commits_dir = CommitsDir.INSTANCE
		commit_dir = commits_dir.get_gitviewfs_object(['a1b2c3d4'])
		
		items = commit_dir.list()
		
		self.assertItemsEqual(['message', 'author', 'committer', 'parents', 'tree'], items)


class TestCommitDirIntegration(TestIntegration):
	
	def test_is_directory(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		commit_dir_path = self.make_commit_dir_path(commit_sha1)
		
		self.assertTrue(os.path.isdir(commit_dir_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
