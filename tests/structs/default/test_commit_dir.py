import os
import subprocess
import unittest

from gitviewfs_objects import Directory
import dir_structure.default
from tests.structs.default import paths
from tests.structs.default.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class CommitDirPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_DIR, Directory)


class CommitDirTest(unittest.TestCase):
	
	def test_get_items_names(self):
		dir_struct = dir_structure.default.Default()
		commit_dir_template = dir_struct.get_commit_dir_template()
		commit_dir = commit_dir_template.create_instance(name='a1b2c3d4')
		
		items = commit_dir.get_items_names()
		
		self.assertItemsEqual(['message', 'author', 'committer', 'parents', 'tree'], items)


class CommitDirIntegrationTest(BaseDefaultDirStructIntegrationTest):
	
	def test_is_directory(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		commit_dir_path = self.make_commit_dir_path(commit_sha1)
		
		self.assertTrue(os.path.isdir(commit_dir_path))
