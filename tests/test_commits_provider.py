import unittest

from gitviewfs_objects import CommitsProvider, OldDirectory


class TestCommitsProvider(unittest.TestCase):
	
	def test_get_item(self):
		provider = CommitsProvider()
		
		NAME = 'name'
		item = provider._get_item(NAME)
		
		self.assertIsInstance(item, OldDirectory)
		self.assertEqual(NAME, item.name)
	
	def test_get_items_names(self):
		provider = CommitsProvider()
		
		items = provider.get_items_names()
		
		self.assertItemsEqual([], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
