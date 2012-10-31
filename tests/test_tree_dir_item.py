import unittest
import subprocess
import os

from tests.test_integration import TestIntegration


class TestTreeDirItem(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestTreeDirItemIntegration(TestIntegration):
	
	def test_tree_dir_items_are_symbolic_links(self):
		filename, subdirname = self.create_and_commit_file_and_subdir()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'])
		tree_sha1 = tree_sha1.strip()
		
		file_path   = self.make_tree_dir_item_path(tree_sha1, filename)
		subdir_path = self.make_tree_dir_item_path(tree_sha1, subdirname)
		
		self.assertTrue(os.path.islink(file_path))
		self.assertTrue(os.path.islink(subdir_path))
	
	def test_readlink_file(self):
		filename, _ = self.create_and_commit_file_and_subdir()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		file_sha1 = subprocess.check_output(['git', 'hash-object', filename]).strip()
		
		item_path = self.make_tree_dir_item_path(tree_sha1, filename)
		
		self.assertSymLink(self.make_blob_file_path(file_sha1), item_path)
	
	def test_readlink_dir(self):
		_, subdirname = self.create_and_commit_file_and_subdir()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		tree_subdir_item = subprocess.check_output('git cat-file -p ' + tree_sha1 + '  |  grep ' + subdirname, shell=True).strip()
		tab_pos = tree_subdir_item.index('\t')
		subdir_sha1 = tree_subdir_item[: tab_pos].split(' ')[2]
		
		item_path = self.make_tree_dir_item_path(tree_sha1, subdirname)
		
		self.assertSymLink(self.make_tree_dir_path(subdir_sha1), item_path)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
