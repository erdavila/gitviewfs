import unittest

from gitviewfs_objects import create_gitviewfs_object, RootDir, RefsDir, HeadSymLink


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


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_get_fs_object_RootDir']
	unittest.main()
