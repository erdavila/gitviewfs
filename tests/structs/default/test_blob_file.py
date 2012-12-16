import subprocess
import unittest

from gitviewfs_objects import get_gitviewfs_object, BlobFile
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration


class TestBlobFile(unittest.TestCase):
	
	def test_path(self):
		blob_file = get_gitviewfs_object(paths.BLOB_FILE)
		
		self.assertIsInstance(blob_file, BlobFile)
		self.assertEqual(paths.BLOB_FILE, blob_file.get_path())


class TestBlobFileIntegration(TestIntegration):
	
	def test_blob_content(self):
		filename, content = self.create_and_commit_file()
		blob_sha1 = subprocess.check_output(['git', 'hash-object', filename]).strip()
		
		blob_path = self.make_blob_file_path(blob_sha1)
		with open(blob_path) as f:
			read_content = f.read()
		
		self.assertEqual(read_content, content)
