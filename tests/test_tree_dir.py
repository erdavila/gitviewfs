import unittest
import os

from tests.test_integration import TestIntegration
from gitviewfs_objects import ObjectsDir, TreesDir
import subprocess


class TestTreeDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def test_get_path(self):
		trees_dir = TreesDir.INSTANCE
		tree_dir = trees_dir.get_gitviewfs_object(['a1b2c3d4'])
		
		path = tree_dir.get_path()
		
		self.assertEqual('/objects/trees/a1b2c3d4', path)


class TestTreeDirIntegration(TestIntegration):
	
	def test_tree_dir_is_directory(self):
		self.create_and_commit_file()
		sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'])
		sha1 = sha1.strip()
		
		tree_dir = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME, sha1)
		
		self.assertTrue(os.path.isdir(tree_dir))
	
	def test_tree_dir_list(self):
		filename, subdirname = self.create_and_commit_file_and_subdir()
		sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'])
		sha1 = sha1.strip()
		
		tree_dir = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME, sha1)
		
		dir_content = os.listdir(tree_dir)
		
		self.assertItemsEqual([filename, subdirname], dir_content)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()