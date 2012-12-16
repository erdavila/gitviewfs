from gitviewfs_objects import get_gitviewfs_object, TreesProvider
from tests.structs.default import paths
from tests.test_with_repository import TestWithRepository


class TestTreesDirWithRepository(TestWithRepository):
	
	def test_path(self):
		trees_dir = get_gitviewfs_object(paths.TREES_DIR)
		
		self.assertIsDirectoryWithProvider(trees_dir, TreesProvider)
		self.assertEqual(paths.TREES_DIR, trees_dir.get_path())
