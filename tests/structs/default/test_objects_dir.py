import os

from gitviewfs_objects import Directory
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class ObjectsDirPathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.OBJECTS_DIR, Directory)


class TestObjectsDirIntegration(TestIntegration):

	def test_list(self):
		refs_dir = self.make_objects_dir_path()
		items = os.listdir(refs_dir)
		self.assertItemsEqual(['blobs', 'commits', 'trees'], items)
