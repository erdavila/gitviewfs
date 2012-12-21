import unittest

from gitviewfs_objects import CommitsProvider, Directory,\
	DIR_STRUCTURE_CONTEXT_NAME
from tests.utils import MockDirStructure


class CommitsProviderTest(unittest.TestCase):
	
	def test_get_item(self):
		provider = CommitsProvider()
		dir_struct = MockDirStructure()
		Directory(name=None, items=[provider], context_values={DIR_STRUCTURE_CONTEXT_NAME:dir_struct})
		
		NAME = 'a-name'
		item = provider._get_item(NAME)
		
		self.assertIsInstance(item, MockDirStructure.Item)
		self.assertEqual(NAME, item.name)
		self.assertEqual('commit_dir_template', item.source)
	
	def test_get_items_names(self):
		provider = CommitsProvider()
		
		items = provider.get_items_names()
		
		self.assertItemsEqual([], items)
