import os
import unittest

from gitviewfs_objects import Directory
import dir_structure.default
from tests.structs.default import paths
from tests.structs.default.utils import DefaultDirStructPathTest,\
	TestIntegration


class RefsDirPathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.REFS_DIR, Directory)
	

class TestRefsDir(unittest.TestCase):

	def test_get_items_names(self):
		dir_struct = dir_structure.default.Default()
		root_dir = dir_struct.get_root_dir()
		refs_dir = root_dir.get_item('refs')
		items = refs_dir.get_items_names()
		
		self.assertItemsEqual(['HEAD', 'branches'], items)


class TestRefsDirIntegration(TestIntegration):
	
	def test_list(self):
		refs_dir_path = self.make_refs_dir_path()
		items = os.listdir(refs_dir_path)
		self.assertItemsEqual(['HEAD', 'branches'], items)
