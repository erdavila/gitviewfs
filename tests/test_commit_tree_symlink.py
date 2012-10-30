import unittest
import stat
import os
import subprocess

from gitviewfs_objects import CommitsDir, CommitTreeSymLink, ObjectsDir
from tests.test_integration import TestIntegration


class TestCommitTreeSymLink(unittest.TestCase):
	
	def test_getattr_returns_symlink_type(self):
		commits_dir = CommitsDir.INSTANCE
		commit_dir = commits_dir.get_gitviewfs_object(['a1b2c3d4'])
		commit_tree_symlink = commit_dir.get_gitviewfs_object([CommitTreeSymLink.NAME])
		
		attr = commit_tree_symlink.getattr()
		
		self.assertTrue(stat.S_ISLNK(attr.st_mode))


class TestCommitTreeSymLinkIntegration(TestIntegration):
	
	def test_is_symlink(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		commit_tree_symlink_path = os.path.join(self.mountpoint, ObjectsDir.NAME, CommitsDir.NAME, commit_sha1, CommitTreeSymLink.NAME)
		
		self.assertTrue(os.path.islink(commit_tree_symlink_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
