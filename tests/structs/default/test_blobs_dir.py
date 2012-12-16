from gitviewfs_objects import get_gitviewfs_object, BlobsProvider
from tests.structs.default import paths
from tests.test_with_repository import TestWithRepository


class TestBlobsDirWithRepository(TestWithRepository):
	
	def test_path(self):
		blobs_dir = get_gitviewfs_object(paths.BLOBS_DIR)
		
		self.assertIsDirectoryWithProvider(blobs_dir, BlobsProvider)
		self.assertEqual(paths.BLOBS_DIR, blobs_dir.get_path())
