import unittest
import subprocess
import os

from tests.test_integration import TestIntegration, TestWithRepository
from gitviewfs_objects import Directory, TreeContextNames, TreeDirItem, BlobFile,\
	TreeDirItemsProvider


class TestTreeDirItemWithRepository(TestWithRepository):

	def setUp(self):
		super(TestTreeDirItemWithRepository, self).setUp()
		self.filename, self.subdirname = self.create_and_commit_file_and_subdir()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		self.context_values = {TreeContextNames.SHA1:tree_sha1}
	
	def test_file_as_blob(self):
		item = TreeDirItem(name=self.filename)
		Directory(name=None, items=[item], context_values=self.context_values)
		
		target = item.get_target_object()
		
		self.assertIsInstance(target, BlobFile)
	
	def test_subdir_as_tree(self):
		item = TreeDirItem(name=self.subdirname)
		Directory(name=None, items=[item], context_values=self.context_values)
		
		target = item.get_target_object()
		
		self.assertIsDirectoryWithProvider(target, TreeDirItemsProvider)
	
	def assertIsDirectoryWithProvider(self, obj, ProviderClass):
		self.assertIsInstance(obj, Directory)
		self.assertTrue(any(isinstance(target_item, TreeDirItemsProvider) for target_item in obj.items))


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
