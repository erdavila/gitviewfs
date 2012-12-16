import os
import unittest

from gitviewfs_objects import get_gitviewfs_object, Directory
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration


class TestObjectsDir(unittest.TestCase):
	
	def test_path(self):
		objects_dir = get_gitviewfs_object(paths.OBJECTS_DIR)
		
		self.assertIsInstance(objects_dir, Directory)
		self.assertEqual(paths.OBJECTS_DIR, objects_dir.get_path())


class TestObjectsDirIntegration(TestIntegration):

	def test_list(self):
		refs_dir = self.make_objects_dir_path()
		items = os.listdir(refs_dir)
		self.assertItemsEqual(['blobs', 'commits', 'trees'], items)
