import os
import unittest

from gitviewfs_objects import COMMITS_DIR, Directory
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class CommitCommitterDirPathTest(DefaultDirStructPathTest):

	def test_path(self):
		self.assertPathIs(paths.COMMIT_COMMITTER_DIR, Directory)


class TestCommitCommitterDir(unittest.TestCase):
	
	def test_get_items_names(self):
		commit_dir = COMMITS_DIR.get_item('a1b2c3d4')
		commit_committer_dir = commit_dir.get_item('committer')
		
		items = commit_committer_dir.get_items_names()
		
		self.assertItemsEqual(['name', 'email', 'date'], items)


class TestCommitCommitterDirIntegration(TestIntegration):
	
	def test_list(self):
		commit_sha1 = paths.SAMPLE_HASH
		commit_committer_dir_path = self.make_commit_committer_dir_path(commit_sha1)
		
		items = os.listdir(commit_committer_dir_path)
		
		self.assertItemsEqual(['name', 'email', 'date'], items)
