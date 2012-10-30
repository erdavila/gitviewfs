import unittest
import os
import subprocess

from tests.test_integration import TestIntegration


class TestTreeDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestTreeDirIntegration(TestIntegration):
	
	def test_is_directory(self):
		self.create_and_commit_file()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		
		tree_dir_path = self.make_tree_dir_path(tree_sha1)
		
		self.assertTrue(os.path.isdir(tree_dir_path))
	
	def test_list(self):
		filename, subdirname = self.create_and_commit_file_and_subdir()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		tree_dir_path = self.make_tree_dir_path(tree_sha1)
		
		dir_content = os.listdir(tree_dir_path)
		
		self.assertItemsEqual([filename, subdirname], dir_content)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()