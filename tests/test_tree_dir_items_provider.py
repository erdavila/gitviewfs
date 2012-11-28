import unittest
import subprocess

from tests.test_integration import TestWithRepository
from gitviewfs_objects import TreeDirItemsProvider, Directory, TreeContextNames,\
	TreeDirItem


class TestTreeDirItemsProviderWithRepository(TestWithRepository):

	def test_get_items_names(self):
		FILE_NAME = 'filename.txt'
		SUBDIR_NAME = 'subdir'
		self.create_and_commit_file(FILE_NAME)
		self.create_and_commit_file(SUBDIR_NAME + '/another-file.txt')
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		
		provider = TreeDirItemsProvider()
		Directory(name=None, items=[provider], context_values={TreeContextNames.SHA1:tree_sha1})
		
		items_names = provider.get_items_names()
		
		self.assertItemsEqual([FILE_NAME, SUBDIR_NAME], items_names)
	

class TestTreeDirItemsProvider(unittest.TestCase):
	
	def test_get_item(self):
		SHA1 = 'a1b2c3d4'
		provider = TreeDirItemsProvider()
		
		item = provider._get_item(SHA1)
		
		self.assertIsInstance(item, TreeDirItem)
		


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()