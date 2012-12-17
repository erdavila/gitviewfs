from gitviewfs_objects import BlobsProvider
from tests.structs.default import paths
from tests.structs.default.utils import DefaultDirStructPathTest


class BlobsDirPathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIsDirectoryWithProvider(paths.BLOBS_DIR, BlobsProvider)
