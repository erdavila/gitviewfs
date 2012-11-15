import unittest

from gitviewfs_objects import DirItemsProvider, Directory, GitViewFSObject


class TestBase(unittest.TestCase):
	
	class MockItem(GitViewFSObject):
		def __init__(self, name):
			self.name = name
	
	class MockDirItemsProvider(DirItemsProvider):
		def __init__(self, items):
			self.items = items
		def get_items_names(self):
			return [item.name for item in self.items]
		def _get_item(self, name):
			for item in self.items:
				if item.name == name:
					return item
	
	def create_directory_with_multiple_items(self):
		self.ITEM_NAME = 'item-name'
		self.mock_item = self.MockItem(self.ITEM_NAME)
		
		self.SUBDIR_NAME = 'dir-name'
		self.subdir = Directory(name=self.SUBDIR_NAME, items=[])
		
		self.PROVIDER_ITEMS_NAMES = ['list-item-1', 'list-item-2']
		self.PROVIDER_ITEMS = [self.MockItem(name) for name in self.PROVIDER_ITEMS_NAMES]
		mock_provider = self.MockDirItemsProvider(self.PROVIDER_ITEMS)
		
		self.directory = Directory(name='', items=[self.mock_item, self.subdir, mock_provider])


class TestDirectoryList(TestBase):
	
	def test_providers_as_items(self):
		ITEMS_NAMES_1 = ('item1', 'item2', 'item3')
		ITEMS_NAMES_2 = 'item4', 'item5'
		mock_provider_1 = self.MockDirItemsProvider(self.MockItem(name) for name in ITEMS_NAMES_1)
		mock_provider_2 = self.MockDirItemsProvider(self.MockItem(name) for name in ITEMS_NAMES_2)
		
		directory = Directory(name='', items=[mock_provider_1, mock_provider_2])
		items = directory.list()
		
		self.assertItemsEqual(ITEMS_NAMES_2 + ITEMS_NAMES_1, items)
	
	def test_directory_as_item(self):
		DIR_NAME = 'dir-name'
		subdir = Directory(name=DIR_NAME, items=[])
		
		directory = Directory(name='', items=[subdir])
		items = directory.list()
		
		self.assertItemsEqual([DIR_NAME], items)
	
	def test_regular_item(self):
		ITEM_NAME = 'name'
		mock_item = self.MockItem(ITEM_NAME)
		
		directory = Directory(name='', items=[mock_item])
		items = directory.list()
		
		self.assertItemsEqual([ITEM_NAME], items)
	
	def test_multiple_content_types(self):
		self.create_directory_with_multiple_items()
		
		items = self.directory.list()
		
		self.assertItemsEqual([self.SUBDIR_NAME, self.ITEM_NAME] + self.PROVIDER_ITEMS_NAMES, items)


class TestDirectoryGetItem(TestBase):
	
	def setUp(self):
		self.create_directory_with_multiple_items()
	
	def test_regular_item(self):
		item = self.directory.get_item(self.ITEM_NAME)
		self.assertIs(item, self.mock_item)
	
	def test_directory_as_item(self):
		item = self.directory.get_item(self.SUBDIR_NAME)
		self.assertIs(item, self.subdir)
	
	def test_item_from_provider(self):
		INDEX = 1
		item = self.directory.get_item(self.PROVIDER_ITEMS_NAMES[INDEX])
		self.assertIs(item, self.PROVIDER_ITEMS[INDEX])


class TestParentDirIsSet(TestBase):
	
	def setUp(self):
		self.create_directory_with_multiple_items()
	
	def test_regular_item(self):
		self.assertIs(self.directory, self.mock_item.parent_dir)
	
	def test_directory_as_item(self):
		self.assertIs(self.directory, self.subdir.parent_dir)
	
	def test_item_from_provider(self):
		for name in self.PROVIDER_ITEMS_NAMES:
			item = self.directory.get_item(name)
			self.assertIs(self.directory, item.parent_dir)


class TestGetPath(TestBase):
	
	def test_root(self):
		ROOT_DIR = Directory(name='does not matter', items=[])
		
		path = ROOT_DIR.get_path()
		
		self.assertEqual('/', path)
	
	def test_child_of_root(self):
		CHILD_NAME = 'child-name'
		child = GitViewFSObject(name=CHILD_NAME)
		_root_dir = Directory(name='does not matter', items=[child])
		
		path = child.get_path()
		
		self.assertEqual('/' + CHILD_NAME, path)
	
	def test_child_of_non_root(self):
		CHILD_NAME = 'child-name'
		child = GitViewFSObject(name=CHILD_NAME)
		
		NON_ROOT_DIR_PATH = 'non-root-dir-path'
		class NonRootDirectory(Directory):
			def get_path(self):
				return NON_ROOT_DIR_PATH
			def is_root(self):
				return False
		_non_root_dir = NonRootDirectory(name='does not matter', items=[child])
		
		path = child.get_path()
		
		self.assertEqual(NON_ROOT_DIR_PATH + '/' + CHILD_NAME, path)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
