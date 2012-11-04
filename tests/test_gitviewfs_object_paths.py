import unittest

from gitviewfs_objects import get_gitviewfs_object, RootDir, RefsDir,\
	HeadSymLink, BranchesDir, BranchSymLink, ObjectsDir, CommitsDir, CommitDir,\
	CommitMessageFile, CommitAuthorDir, CommitAuthorNameFile, CommitTreeSymLink,\
	TreesDir, TreeDir, TreeDirItem, BlobsDir, BlobFile
from tests import paths


class TestPaths(unittest.TestCase):
	
	def assertPathClass(self, path, Class):
		obj = get_gitviewfs_object(path)
		self.assertIsInstance(obj, Class)
		
		result = obj.get_path()
		self.assertEqual(path, result)
	
	def assertPathClassAndName(self, path, Class, name=None):
		obj = get_gitviewfs_object(path)
		self.assertIsInstance(obj, Class)
		expected_name = Class.NAME if name is None else name
		self.assertEqual(expected_name, obj.name)
		
		result = obj.get_path()
		self.assertEqual(path, result)
	
	def test_RootDir(self):
		self.assertPathClass(paths.ROOT_DIR, RootDir)
	
	def test_RefsDir(self):
		self.assertPathClassAndName(paths.REFS_DIR, RefsDir)
	
	def test_HeadSymLink(self):
		self.assertPathClassAndName(paths.HEAD_SYMLINK, HeadSymLink)
	
	def test_BranchesDir(self):
		self.assertPathClassAndName(paths.BRANCHES_DIR, BranchesDir)
	
	def test_BranchSymLink(self):
		self.assertPathClassAndName(paths.BRANCH_SYMLINK, BranchSymLink, paths.SAMPLE_BRANCH)
	
	def test_ObjectsDir(self):
		self.assertPathClassAndName(paths.OBJECTS_DIR, ObjectsDir)
	
	def test_CommitsDir(self):
		self.assertPathClassAndName(paths.COMMITS_DIR, CommitsDir)
	
	def test_CommitDir(self):
		self.assertPathClassAndName(paths.COMMIT_DIR, CommitDir, paths.SAMPLE_HASH)
	
	def test_CommitMessageFile(self):
		self.assertPathClassAndName(paths.COMMIT_MESSAGE_FILE, CommitMessageFile)
	
	def test_CommitAuthorDir(self):
		self.assertPathClassAndName(paths.COMMIT_AUTHOR_DIR, CommitAuthorDir)
	
	def test_CommitAuthorNameFile(self):
		self.assertPathClassAndName(paths.COMMIT_AUTHOR_NAME_FILE, CommitAuthorNameFile)
	
	def test_CommitTreeSymLink(self):
		self.assertPathClassAndName(paths.COMMIT_TREE_SYMLINK, CommitTreeSymLink)
	
	def test_TreesDir(self):
		self.assertPathClassAndName(paths.TREES_DIR, TreesDir)
	
	def test_TreeDir(self):
		self.assertPathClassAndName(paths.TREE_DIR, TreeDir, paths.SAMPLE_HASH)
	
	def test_TreeDirItem(self):
		self.assertPathClassAndName(paths.TREE_DIR_ITEM, TreeDirItem, paths.SAMPLE_FILENAME)
	
	def test_BlobsDir(self):
		self.assertPathClassAndName(paths.BLOBS_DIR, BlobsDir)
	
	def test_BlobFile(self):
		self.assertPathClassAndName(paths.BLOB_FILE, BlobFile, paths.SAMPLE_HASH)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_get_fs_object_RootDir']
	unittest.main()
