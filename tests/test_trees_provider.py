import unittest

from gitviewfs_objects import TreesProvider, Directory


class TestTreesProvider(unittest.TestCase):

	def test_get_items_names(self):
		provider = TreesProvider()
		
		items_names = provider.get_items_names()
		
		self.assertItemsEqual([], items_names)
	
	def test_get_item(self):
		provider = TreesProvider()
		
		ITEM_NAME = 'a1b2c3d4'
		item = provider._get_item(ITEM_NAME)
		
		self.assertIsInstance(item, Directory)
		self.assertEqual(ITEM_NAME, item.name)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
