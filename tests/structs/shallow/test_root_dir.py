import os
import unittest

from gitviewfs_objects import Directory
import dir_structure.shallow
from tests.structs.shallow import paths
from tests.structs.shallow.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class RootDirPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.ROOT_DIR, Directory)


class RootDirTest(unittest.TestCase):

	def test_get_items_names(self):
		dir_struct = dir_structure.shallow.Shallow()
		root_dir = dir_struct.get_root_dir()
		items = root_dir.get_items_names()
		
		self.assertItemsEqual(['HEAD', 'branches', 'commits', 'trees', 'blobs'], items)


class RootDirIntegrationTest(BaseDefaultDirStructIntegrationTest):
	
	def test_list(self):
		items = os.listdir(self.mountpoint)
		
		self.assertItemsEqual(['HEAD', 'branches', 'commits', 'trees', 'blobs'], items)
