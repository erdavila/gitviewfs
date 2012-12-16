import os
import unittest

from gitviewfs_objects import ROOT_DIR, get_gitviewfs_object, Directory
from tests.structs.default.test_integration import TestIntegration
from tests.structs.default import paths


class TestRootDir(unittest.TestCase):
	
	def test_path(self):
		root_dir = get_gitviewfs_object(paths.ROOT_DIR)
		
		self.assertIsInstance(root_dir, Directory)
		self.assertEqual(paths.ROOT_DIR, root_dir.get_path())

	def test_get_items_names(self):
		items = ROOT_DIR.get_items_names()
		
		self.assertItemsEqual(['refs', 'objects'], items)


class TestRootDirIntegration(TestIntegration):
	
	def test_list(self):
		items = os.listdir(self.mountpoint)
		
		self.assertItemsEqual(['refs', 'objects'], items)
