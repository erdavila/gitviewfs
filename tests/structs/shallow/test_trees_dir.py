from gitviewfs_objects import TreesProvider
from tests.structs.shallow import paths
from tests.structs.shallow.utils import BaseDefaultDirStructTest


class TreesDirPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIsDirectoryWithProvider(paths.TREES_DIR, TreesProvider)
