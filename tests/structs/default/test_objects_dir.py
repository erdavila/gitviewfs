import os

from gitviewfs_objects import Directory
from tests.structs.default import paths
from tests.structs.default.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class ObjectsDirPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.OBJECTS_DIR, Directory)


class ObjectsDirIntegrationTest(BaseDefaultDirStructIntegrationTest):

	def test_list(self):
		refs_dir = self.make_objects_dir_path()
		items = os.listdir(refs_dir)
		self.assertItemsEqual(['blobs', 'commits', 'trees'], items)
