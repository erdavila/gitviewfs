import unittest

from gitviewfs_objects import create_gitviewfs_object, RootDir, RefsDir, HeadSymLink,\
	ObjectsDir, BlobsDir, BlobFile, TreesDir, TreeDir


class TestCreateGitViewFSObject(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_create_fs_object_RootDir(self):
		obj = create_gitviewfs_object("/")
		self.assertIsInstance(obj, RootDir)
	
	def test_create_fs_object_RefsDir(self):
		obj = create_gitviewfs_object("/refs")
		self.assertIsInstance(obj, RefsDir)
	
	def test_create_fs_object_HeadSymLink(self):
		obj = create_gitviewfs_object("/refs/HEAD")
		self.assertIsInstance(obj, HeadSymLink)
	
	def test_create_fs_object_ObjectsDir(self):
		obj = create_gitviewfs_object("/objects")
		self.assertIsInstance(obj, ObjectsDir)
	
	def test_create_fs_object_TreesDir(self):
		obj = create_gitviewfs_object("/objects/trees")
		self.assertIsInstance(obj, TreesDir)
	
	def test_create_fs_object_TreeDir(self):
		sha1 = '0123456789abcdef0123456789abcdef01234567'
		obj = create_gitviewfs_object("/objects/trees/" + sha1)
		self.assertIsInstance(obj, TreeDir)
		self.assertEqual(obj.name, sha1)
	
	def test_create_fs_object_TreeFile_abbrev(self):
		sha1 = '0123'
		obj = create_gitviewfs_object("/objects/trees/" + sha1)
		self.assertIsInstance(obj, TreeDir)
		self.assertEqual(obj.name, sha1)
	
	def test_create_fs_object_BlobsDir(self):
		obj = create_gitviewfs_object("/objects/blobs")
		self.assertIsInstance(obj, BlobsDir)
	
	def test_create_fs_object_BlobFile(self):
		sha1 = '0123456789abcdef0123456789abcdef01234567'
		obj = create_gitviewfs_object("/objects/blobs/" + sha1)
		self.assertIsInstance(obj, BlobFile)
		self.assertEqual(obj.name, sha1)
	
	def test_create_fs_object_BlobFile_abbrev(self):
		sha1 = '0123'
		obj = create_gitviewfs_object("/objects/blobs/" + sha1)
		self.assertIsInstance(obj, BlobFile)
		self.assertEqual(obj.name, sha1)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_get_fs_object_RootDir']
	unittest.main()
