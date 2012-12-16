import os
import subprocess

from gitviewfs_objects import get_gitviewfs_object, TreeDirItemsProvider
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration
from tests.test_with_repository import TestBase


class TestTreeDir(TestBase):
	
	def test_path(self):
		tree_dir = get_gitviewfs_object(paths.TREE_DIR)
		
		self.assertIsDirectoryWithProvider(tree_dir, TreeDirItemsProvider)
		self.assertEqual(paths.TREE_DIR, tree_dir.get_path())


class TestTreeDirIntegration(TestIntegration):
	
	def test_list(self):
		filename, subdirname = self.create_and_commit_file_and_subdir()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		tree_dir_path = self.make_tree_dir_path(tree_sha1)
		
		dir_content = os.listdir(tree_dir_path)
		
		self.assertItemsEqual([filename, subdirname], dir_content)
