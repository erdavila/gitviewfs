import unittest

from gitviewfs_objects import DirItemsProvider, Directory


class TestBase(unittest.TestCase):
	
	class MockItem(object):
		def __init__(self, name):
			self.name = name
	
	class MockDirItemsProvider(DirItemsProvider):
		def __init__(self, items):
			self.items = items
		def get_items_names(self):
			return [item.name for item in self.items]
		def get_item(self, name):
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

	def setUp(self):
		pass

	def tearDown(self):
		pass
	
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


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
