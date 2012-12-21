import subprocess

from gitviewfs_objects import BlobFile
from tests.structs.default import paths
from tests.structs.default.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class BlobFileTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.BLOB_FILE, BlobFile)


class BlobFileIntegrationTest(BaseDefaultDirStructIntegrationTest):
	
	def test_blob_content(self):
		filename, content = self.create_and_commit_file()
		blob_sha1 = subprocess.check_output(['git', 'hash-object', filename]).strip()
		
		blob_path = self.make_blob_file_path(blob_sha1)
		with open(blob_path) as f:
			read_content = f.read()
		
		self.assertEqual(read_content, content)
