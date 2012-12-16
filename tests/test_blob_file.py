import subprocess

from gitviewfs_objects import BlobFile
from tests.test_with_repository import TestWithRepository


class TestBlobFileWithRepository(TestWithRepository):

	def test_get_content(self):
		filename, content = self.create_and_commit_file()
		file_sha1 = subprocess.check_output(['git', 'hash-object', filename]).strip()
		
		blob_file = BlobFile(name=file_sha1)
		
		self.assertEqual(content, blob_file.get_content())
	
	def test_get_content_size_should_not_call_get_content(self):
		filename, content = self.create_and_commit_file()
		file_sha1 = subprocess.check_output(['git', 'hash-object', filename]).strip()
		
		blob_file = BlobFile(name=file_sha1)
		def get_content(*args, **kwargs):
			self.fail("get_content() should not be called by _get_content_size()")
		blob_file.get_content = get_content
		
		self.assertEqual(len(content), blob_file._get_content_size())
