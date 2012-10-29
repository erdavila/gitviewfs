import unittest
import os
import subprocess

from tests.test_integration import TestIntegration
from gitviewfs_objects import ObjectsDir, TreesDir


class TestTreeDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestTreeDirIntegration(TestIntegration):
	
	def test_is_directory(self):
		self.create_and_commit_file()
		sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'])
		sha1 = sha1.strip()
		
		tree_dir = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME, sha1)
		
		self.assertTrue(os.path.isdir(tree_dir))
	
	def test_list(self):
		filename, subdirname = self.create_and_commit_file_and_subdir()
		sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'])
		sha1 = sha1.strip()
		
		tree_dir = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME, sha1)
		
		dir_content = os.listdir(tree_dir)
		
		self.assertItemsEqual([filename, subdirname], dir_content)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()