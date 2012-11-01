import unittest
import stat
import os
import subprocess

from gitviewfs_objects import get_gitviewfs_object
from tests.test_integration import TestIntegration
from tests import paths


class TestCommitTreeSymLink(unittest.TestCase):
	
	def test_getattr_returns_symlink_type(self):
		commit_tree_symlink = get_gitviewfs_object(paths.COMMIT_TREE_SYMLINK)
		
		attr = commit_tree_symlink.getattr()
		
		self.assertTrue(stat.S_ISLNK(attr.st_mode))


class TestCommitTreeSymLinkIntegration(TestIntegration):
	
	def test_is_symlink(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		commit_tree_symlink_path = self.make_commit_tree_symlink_path(commit_sha1)
		
		self.assertTrue(os.path.islink(commit_tree_symlink_path))
	
	def test_readlink(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		commit_tree_symlink_path = self.make_commit_tree_symlink_path(commit_sha1)
		
		self.assertSymLink(self.make_tree_dir_path(tree_sha1), commit_tree_symlink_path)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()