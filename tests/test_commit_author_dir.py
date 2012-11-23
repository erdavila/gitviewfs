import unittest
import stat
import os.path

from gitviewfs_objects import COMMITS_DIR
from tests.test_integration import TestIntegration
from tests import paths


class TestCommitAuthorDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_is_directory(self):
		commit_author_dir = self.make_commit_author_dir_object()
		
		attr = commit_author_dir.getattr()
		
		self.assertTrue(stat.S_ISDIR(attr.st_mode))
	
	def test_list(self):
		commit_author_dir = self.make_commit_author_dir_object()
		
		items = commit_author_dir.list()
		
		self.assertItemsEqual(['name', 'email', 'date'], items)
	
	def make_commit_author_dir_object(self):
		commit_dir = COMMITS_DIR.get_item('a1b2c3d4')
		commit_author_dir = commit_dir.get_item('author')
		return commit_author_dir


class TestCommitAuthorDirIntegration(TestIntegration):
	
	def test_is_directory(self):
		commit_sha1 = paths.SAMPLE_HASH
		commit_author_dir_path = self.make_commit_author_dir_path(commit_sha1)
		
		self.assertTrue(os.path.isdir(commit_author_dir_path))
	
	def test_list(self):
		commit_sha1 = paths.SAMPLE_HASH
		commit_author_dir_path = self.make_commit_author_dir_path(commit_sha1)
		
		items = os.listdir(commit_author_dir_path)
		
		self.assertItemsEqual(['name', 'email', 'date'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()