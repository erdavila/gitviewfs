import os
import subprocess
import unittest

from gitviewfs_objects import Directory, COMMIT_DIR_TEMPLATE
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class CommitDirPathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_DIR, Directory)


class TestCommitDir(unittest.TestCase):
	
	def test_get_items_names(self):
		commit_dir = COMMIT_DIR_TEMPLATE.create_instance(name='a1b2c3d4')
		
		items = commit_dir.get_items_names()
		
		self.assertItemsEqual(['message', 'author', 'committer', 'parents', 'tree'], items)


class TestCommitDirIntegration(TestIntegration):
	
	def test_is_directory(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		commit_dir_path = self.make_commit_dir_path(commit_sha1)
		
		self.assertTrue(os.path.isdir(commit_dir_path))
