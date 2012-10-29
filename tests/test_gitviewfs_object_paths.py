import unittest

from gitviewfs_objects import get_gitviewfs_object, RootDir, RefsDir,\
	HeadSymLink, ObjectsDir, CommitsDir, CommitDir, TreesDir, TreeDir, TreeDirItem,\
	BlobsDir, BlobFile


SAMPLE_HASH = 'a1b2c3d4'
SAMPLE_FILENAME = 'filename'

class Path(object):
	ROOT_DIR      = '/'
	REFS_DIR      = '/refs'
	HEAD_SYMLINK  = '/refs/HEAD'
	OBJECTS_DIR   = '/objects'
	COMMITS_DIR   = '/objects/commits'
	COMMIT_DIR    = '/objects/commits/' + SAMPLE_HASH
	TREES_DIR     = '/objects/trees'
	TREE_DIR      = '/objects/trees/' + SAMPLE_HASH
	TREE_DIR_ITEM = '/objects/trees/' + SAMPLE_HASH + '/' + SAMPLE_FILENAME
	BLOBS_DIR     = '/objects/blobs'
	BLOB_FILE     = '/objects/blobs/' + SAMPLE_HASH


class TestGetGitViewFSObject(unittest.TestCase):

	def test_RootDir(self):
		obj = get_gitviewfs_object(Path.ROOT_DIR)
		self.assertIsInstance(obj, RootDir)
	
	def test_RefsDir(self):
		obj = get_gitviewfs_object(Path.REFS_DIR)
		self.assertIsInstance(obj, RefsDir)
	
	def test_HeadSymLink(self):
		obj = get_gitviewfs_object(Path.HEAD_SYMLINK)
		self.assertIsInstance(obj, HeadSymLink)
	
	def test_ObjectsDir(self):
		obj = get_gitviewfs_object(Path.OBJECTS_DIR)
		self.assertIsInstance(obj, ObjectsDir)
	
	def test_CommitsDir(self):
		obj = get_gitviewfs_object(Path.COMMITS_DIR)
		self.assertIsInstance(obj, CommitsDir)
	
	def test_CommitDir(self):
		obj = get_gitviewfs_object(Path.COMMIT_DIR)
		self.assertIsInstance(obj, CommitDir)
		self.assertEqual(obj.name, SAMPLE_HASH)
	
	def test_TreesDir(self):
		obj = get_gitviewfs_object(Path.TREES_DIR)
		self.assertIsInstance(obj, TreesDir)
	
	def test_TreeDir(self):
		obj = get_gitviewfs_object(Path.TREE_DIR)
		self.assertIsInstance(obj, TreeDir)
		self.assertEqual(obj.name, SAMPLE_HASH)
	
	def test_TreeDirItem(self):
		obj = get_gitviewfs_object(Path.TREE_DIR_ITEM)
		self.assertIsInstance(obj, TreeDirItem)
		self.assertEqual(SAMPLE_FILENAME, obj.name)
	
	def test_BlobsDir(self):
		obj = get_gitviewfs_object(Path.BLOBS_DIR)
		self.assertIsInstance(obj, BlobsDir)
	
	def test_BlobFile(self):
		obj = get_gitviewfs_object(Path.BLOB_FILE)
		self.assertIsInstance(obj, BlobFile)
		self.assertEqual(obj.name, SAMPLE_HASH)


class TestGetPath(unittest.TestCase):
	
	def test_RootDir(self):
		root_dir = RootDir.INSTANCE
		path = root_dir.get_path()
		self.assertEqual(Path.ROOT_DIR, path)
	
	def test_RefsDir(self):
		refs_dir = RefsDir.INSTANCE
		path = refs_dir.get_path()
		self.assertEqual(Path.REFS_DIR, path)
	
	def test_HeadSymLink(self):
		head_symlink = HeadSymLink.INSTANCE
		path = head_symlink.get_path()
		self.assertEqual(Path.HEAD_SYMLINK, path)
	
	def test_ObjectsDir(self):
		objects_dir = ObjectsDir.INSTANCE
		path = objects_dir.get_path()
		self.assertEqual(Path.OBJECTS_DIR, path)
	
	def test_CommitsDir(self):
		commits_dir = CommitsDir.INSTANCE
		path = commits_dir.get_path()
		self.assertEqual(Path.COMMITS_DIR, path)

	def test_CommitDir(self):
		commits_dir = CommitsDir.INSTANCE
		commit_dir = commits_dir.get_gitviewfs_object([SAMPLE_HASH])
		path = commit_dir.get_path()
		self.assertEqual(Path.COMMIT_DIR, path)
	
	def test_TreesDir(self):
		trees_dir = TreesDir.INSTANCE
		path = trees_dir.get_path()
		self.assertEqual(Path.TREES_DIR, path)
	
	def test_TreeDir(self):
		trees_dir = TreesDir.INSTANCE
		tree_dir = trees_dir.get_gitviewfs_object([SAMPLE_HASH])
		path = tree_dir.get_path()
		self.assertEqual(Path.TREE_DIR, path)
	
	def test_TreeDirItem(self):
		trees_dir = TreesDir.INSTANCE
		tree_dir = trees_dir.get_gitviewfs_object([SAMPLE_HASH])
		tree_dir_item = tree_dir.get_gitviewfs_object([SAMPLE_FILENAME])
		path = tree_dir_item.get_path()
		self.assertEqual(Path.TREE_DIR_ITEM, path)
	
	def test_BlobsDir(self):
		blobs_dir = BlobsDir.INSTANCE
		path = blobs_dir.get_path()
		self.assertEqual(Path.BLOBS_DIR, path)
	
	def test_BlobDir(self):
		blobs_dir = BlobsDir.INSTANCE
		blob_file = blobs_dir.get_gitviewfs_object([SAMPLE_HASH])
		path = blob_file.get_path()
		self.assertEqual(Path.BLOB_FILE, path)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_get_fs_object_RootDir']
	unittest.main()
