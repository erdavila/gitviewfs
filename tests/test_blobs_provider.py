import unittest
from gitviewfs_objects import BlobsProvider, BlobFile


class BlobsProviderTest(unittest.TestCase):

	def test_get_items_names(self):
		provider = BlobsProvider()
		
		items = provider.get_items_names()
		
		self.assertItemsEqual([], items)
	
	def test_get_item(self):
		provider = BlobsProvider()
		
		NAME = 'a1b2c3d4'
		item = provider._get_item(NAME)
		
		self.assertIsInstance(item, BlobFile)
		self.assertEqual(NAME, item.name)
