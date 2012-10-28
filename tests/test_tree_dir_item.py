import unittest
from tests.test_integration import TestIntegration
import subprocess
import os
from gitviewfs_objects import ObjectsDir, TreesDir


class TestTreeDirItem(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestTreeDirItemIntegration(TestIntegration):
	
	def test_tree_dir_items_are_symbolic_links(self):
		filename, subdirname = self.create_and_commit_file_and_subdir()
		sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'])
		sha1 = sha1.strip()
		
		file_path = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME, sha1, filename)
		self.assertTrue(os.path.islink(file_path))
		
		subdir_path = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME, sha1, subdirname)
		self.assertTrue(os.path.islink(subdir_path))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
