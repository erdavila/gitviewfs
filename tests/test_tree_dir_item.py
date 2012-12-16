import subprocess

from tests.test_with_repository import TestWithRepository
from gitviewfs_objects import Directory, TreeContextNames, TreeDirItem, BlobFile,\
	TreeDirItemsProvider


class TestTreeDirItemWithRepository(TestWithRepository):

	def setUp(self):
		super(TestTreeDirItemWithRepository, self).setUp()
		self.filename, self.subdirname = self.create_and_commit_file_and_subdir()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		self.context_values = {TreeContextNames.SHA1:tree_sha1}
	
	def test_file_as_blob(self):
		item = TreeDirItem(name=self.filename)
		Directory(name=None, items=[item], context_values=self.context_values)
		
		target = item.get_target_object()
		
		self.assertIsInstance(target, BlobFile)
	
	def test_subdir_as_tree(self):
		item = TreeDirItem(name=self.subdirname)
		Directory(name=None, items=[item], context_values=self.context_values)
		
		target = item.get_target_object()
		
		self.assertIsDirectoryWithProvider(target, TreeDirItemsProvider)
