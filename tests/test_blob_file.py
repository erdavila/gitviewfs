import unittest
import subprocess
import os
import stat

from gitviewfs_objects import ObjectsDir, BlobsDir, get_gitviewfs_object
from tests.test_integration import TestIntegration


class TestBlobFile(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def test_get_path(self):
		blobs_dir = BlobsDir.INSTANCE
		blob_file = blobs_dir.get_gitviewfs_object(['a1b2c3d4'])
		
		path = blob_file.get_path()
		
		self.assertEqual('/objects/blobs/a1b2c3d4', path)


class TestBlobFileIntegration(TestIntegration):
	
	def test_blob_content(self):
		filename, content = self.create_and_commit_file()
		sha1 = subprocess.check_output(['git', 'hash-object', filename])
		sha1 = sha1.strip()
		
		blob_path = os.path.join(self.mountpoint, ObjectsDir.NAME, BlobsDir.NAME, sha1)
		with open(blob_path) as f:
			read_content = f.read()
		
		self.assertEqual(read_content, content)
	
	def test_blob_attributes(self):
		filename, content = self.create_and_commit_file()
		sha1 = subprocess.check_output(['git', 'hash-object', filename])
		sha1 = sha1.strip()
		blob_path = os.path.join(self.mountpoint, ObjectsDir.NAME, BlobsDir.NAME, sha1)
		
		st = os.stat(blob_path)
		
		self.assertEqual(st.st_size, len(content))
		
		self.assertFalse(st.st_mode & stat.S_IXUSR)
		self.assertFalse(st.st_mode & stat.S_IXGRP)
		self.assertFalse(st.st_mode & stat.S_IXOTH)
	
	def test_blob_is_regular_file(self):
		filename, _ = self.create_and_commit_file()
		sha1 = subprocess.check_output(['git', 'hash-object', filename])
		sha1 = sha1.strip()
		
		blob_path = os.path.join(self.mountpoint, ObjectsDir.NAME, BlobsDir.NAME, sha1)
		
		self.assertTrue(os.path.isfile(blob_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
