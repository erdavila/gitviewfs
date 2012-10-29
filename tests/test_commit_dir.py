import unittest
import os
import subprocess

from tests.test_integration import TestIntegration
from gitviewfs_objects import ObjectsDir, TreesDir, CommitsDir


class TestCommitDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def test_get_path(self):
		commits_dir = CommitsDir.INSTANCE
		commit_dir = commits_dir.get_gitviewfs_object(['a1b2c3d4'])
		
		path = commit_dir.get_path()
		
		self.assertEqual('/objects/commits/a1b2c3d4', path)
	
	def test_list(self):
		commits_dir = CommitsDir.INSTANCE
		commit_dir = commits_dir.get_gitviewfs_object(['a1b2c3d4'])
		
		items = commit_dir.list()
		
		self.assertItemsEqual(['message', 'author', 'committer', 'parents', 'tree'], items)


class TestCommitDirIntegration(TestIntegration):
	
	def test_is_directory(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		commit_dir = os.path.join(self.mountpoint, ObjectsDir.NAME, CommitsDir.NAME, commit_sha1)
		
		self.assertTrue(os.path.isdir(commit_dir))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
