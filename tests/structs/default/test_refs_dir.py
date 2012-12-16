import os
import unittest

from gitviewfs_objects import get_gitviewfs_object, Directory, ROOT_DIR
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration


class TestRefsDir(unittest.TestCase):
	
	def test_path(self):
		refs_dir = get_gitviewfs_object(paths.REFS_DIR)
		
		self.assertIsInstance(refs_dir, Directory)
		self.assertEqual(paths.REFS_DIR, refs_dir.get_path())

	def test_get_items_names(self):
		refs_dir = ROOT_DIR.get_item('refs')
		items = refs_dir.get_items_names()
		
		self.assertItemsEqual(['HEAD', 'branches'], items)


class TestRefsDirIntegration(TestIntegration):
	
	def test_list(self):
		refs_dir_path = self.make_refs_dir_path()
		items = os.listdir(refs_dir_path)
		self.assertItemsEqual(['HEAD', 'branches'], items)
