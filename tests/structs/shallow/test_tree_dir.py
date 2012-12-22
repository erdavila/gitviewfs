import os
import subprocess

from gitviewfs_objects import TreeDirItemsProvider
from tests.structs.shallow import paths
from tests.structs.shallow.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class TreeDirPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIsDirectoryWithProvider(paths.TREE_DIR, TreeDirItemsProvider)


class TreeDirIntegrationTest(BaseDefaultDirStructIntegrationTest):
	
	def test_list(self):
		filename, subdirname = self.create_and_commit_file_and_subdir()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		tree_dir_path = self.make_tree_dir_path(tree_sha1)
		
		dir_content = os.listdir(tree_dir_path)
		
		self.assertItemsEqual([filename, subdirname], dir_content)
