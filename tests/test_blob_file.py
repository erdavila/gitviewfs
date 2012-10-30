import unittest
import subprocess
import os
import stat

from tests.test_integration import TestIntegration


class TestBlobFile(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


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
