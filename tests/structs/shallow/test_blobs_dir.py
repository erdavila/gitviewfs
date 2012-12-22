from gitviewfs_objects import BlobsProvider
from tests.structs.shallow import paths
from tests.structs.shallow.utils import BaseDefaultDirStructTest


class BlobsDirPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIsDirectoryWithProvider(paths.BLOBS_DIR, BlobsProvider)
