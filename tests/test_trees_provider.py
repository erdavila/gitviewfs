import unittest

from gitviewfs_objects import TreesProvider, Directory,\
	DIR_STRUCTURE_CONTEXT_NAME
from tests.test_with_repository import MockDirStructure


class TestTreesProvider(unittest.TestCase):

	def test_get_items_names(self):
		provider = TreesProvider()
		
		items_names = provider.get_items_names()
		
		self.assertItemsEqual([], items_names)
	
	def test_get_item(self):
		dir_struct = MockDirStructure()
		
		provider = TreesProvider()
		Directory(name=None, items=[provider], context_values={DIR_STRUCTURE_CONTEXT_NAME:dir_struct})
		
		ITEM_NAME = 'a1b2c3d4'
		item = provider._get_item(ITEM_NAME)
		
		self.assertIsInstance(item, MockDirStructure.Item)
		self.assertEqual(ITEM_NAME, item.name)
		self.assertEqual('tree_dir_template', item.source)
