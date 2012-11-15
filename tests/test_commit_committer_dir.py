import unittest
import stat
import os.path

from gitviewfs_objects import COMMITS_DIR
from tests.test_integration import TestIntegration
from tests import paths


class TestCommitCommitterDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_is_directory(self):
		commit_committer_dir = self.make_commit_committer_dir_object()
		
		attr = commit_committer_dir.getattr()
		
		self.assertTrue(stat.S_ISDIR(attr.st_mode))
	
	def test_list(self):
		commit_committer_dir = self.make_commit_committer_dir_object()
		
		items = commit_committer_dir.list()
		
		self.assertItemsEqual(['name', 'email', 'date'], items)
	
	def make_commit_committer_dir_object(self):
		commit_dir = COMMITS_DIR.get_item('a1b2c3d4')
		commit_comitter_dir = commit_dir.get_gitviewfs_object(['committer'])
		return commit_comitter_dir


class TestCommitCommitterDirIntegration(TestIntegration):
	
	def test_is_directory(self):
		commit_sha1 = paths.SAMPLE_HASH
		commit_committer_dir_path = self.make_commit_committer_dir_path(commit_sha1)
		
		self.assertTrue(os.path.isdir(commit_committer_dir_path))
	
	def test_list(self):
		commit_sha1 = paths.SAMPLE_HASH
		commit_committer_dir_path = self.make_commit_committer_dir_path(commit_sha1)
		
		items = os.listdir(commit_committer_dir_path)
		
		self.assertItemsEqual(['name', 'email', 'date'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
