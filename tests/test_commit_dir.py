import unittest
import os
import subprocess

from tests.test_integration import TestIntegration
from gitviewfs_objects import get_gitviewfs_object
from tests import paths


class TestCommitDir(unittest.TestCase):
	
	def test_get_items_names(self):
		commit_dir = get_gitviewfs_object(paths.COMMIT_DIR)
		
		items = commit_dir.get_items_names()
		
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
