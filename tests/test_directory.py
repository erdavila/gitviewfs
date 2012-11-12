import unittest

from gitviewfs_objects import DirItemsProvider, Directory


class TestDirectoryList(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	class MockItem(object):
		def __init__(self, name):
			self.name = name
	
	class MockDirItemsProvider(DirItemsProvider):
		def __init__(self, items):
			self.items = items
		def get_items_names(self):
			return [item.name for item in self.items]
	
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
		ITEM_NAME = 'item-name'
		mock_item = self.MockItem(ITEM_NAME)
		
		SUBDIR_NAME = 'dir-name'
		subdir = Directory(name=SUBDIR_NAME, items=[])
		
		ITEMS_NAMES = ['list-item-1', 'list-item-2']
		mock_provider = self.MockDirItemsProvider(self.MockItem(name) for name in ITEMS_NAMES)
		
		directory = Directory(name='', items=[mock_item, subdir, mock_provider])
		items = directory.list()
		
		self.assertItemsEqual([SUBDIR_NAME, ITEM_NAME] + ITEMS_NAMES, items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
