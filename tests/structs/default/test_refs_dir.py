import os
import unittest

from gitviewfs_objects import Directory, ROOT_DIR
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class RefsDirPathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.REFS_DIR, Directory)
	

class TestRefsDir(unittest.TestCase):

	def test_get_items_names(self):
		refs_dir = ROOT_DIR.get_item('refs')
		items = refs_dir.get_items_names()
		
		self.assertItemsEqual(['HEAD', 'branches'], items)


class TestRefsDirIntegration(TestIntegration):
	
	def test_list(self):
		refs_dir_path = self.make_refs_dir_path()
		items = os.listdir(refs_dir_path)
		self.assertItemsEqual(['HEAD', 'branches'], items)
