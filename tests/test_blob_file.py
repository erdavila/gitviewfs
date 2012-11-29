import unittest
import subprocess
import os
import stat

from tests.test_integration import TestIntegration, TestWithRepository
from gitviewfs_objects import BlobFile


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


class TestBlobFileIntegration(TestIntegration):
	
	def test_blob_content(self):
		filename, content = self.create_and_commit_file()
		blob_sha1 = subprocess.check_output(['git', 'hash-object', filename]).strip()
		
		blob_path = self.make_blob_file_path(blob_sha1)
		with open(blob_path) as f:
			read_content = f.read()
		
		self.assertEqual(read_content, content)
	
	def test_blob_attributes(self):
		filename, content = self.create_and_commit_file()
		blob_sha1 = subprocess.check_output(['git', 'hash-object', filename]).strip()
		blob_path = self.make_blob_file_path(blob_sha1)
		
		st = os.stat(blob_path)
		
		self.assertEqual(st.st_size, len(content))
		
		self.assertFalse(st.st_mode & stat.S_IXUSR)
		self.assertFalse(st.st_mode & stat.S_IXGRP)
		self.assertFalse(st.st_mode & stat.S_IXOTH)
	
	def test_blob_is_regular_file(self):
		filename, _ = self.create_and_commit_file()
		blob_sha1 = subprocess.check_output(['git', 'hash-object', filename]).strip()
		
		blob_path = self.make_blob_file_path(blob_sha1)
		
		self.assertTrue(os.path.isfile(blob_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
