from gitviewfs_objects import TreesProvider
from tests.structs.default import paths
from tests.structs.default.utils import BaseDefaultDirStructTest


class TreesDirPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIsDirectoryWithProvider(paths.TREES_DIR, TreesProvider)
