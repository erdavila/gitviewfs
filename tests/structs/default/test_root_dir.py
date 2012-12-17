import os
import unittest

from gitviewfs_objects import Directory
import dir_structure.default
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class RootDirPathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.ROOT_DIR, Directory)


class TestRootDir(unittest.TestCase):

	def test_get_items_names(self):
		dir_struct = dir_structure.default.Default()
		root_dir = dir_struct.get_root_dir()
		items = root_dir.get_items_names()
		
		self.assertItemsEqual(['refs', 'objects'], items)


class TestRootDirIntegration(TestIntegration):
	
	def test_list(self):
		items = os.listdir(self.mountpoint)
		
		self.assertItemsEqual(['refs', 'objects'], items)
