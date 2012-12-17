import subprocess

from tests.test_with_repository import TestWithRepository, MockDirStructure
from gitviewfs_objects import Directory, TreeContextNames, TreeDirItem, BlobFile,\
	TreeDirItemsProvider, DIR_STRUCTURE_CONTEXT_NAME
from git_objects_parser import GitCommitParser, GitTreeParser


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
		
		parser = GitTreeParser()
		tree_items = parser.parse('HEAD^{tree}')
		subdir_sha1 = tree_items[self.subdirname].sha1
		
		context_values = self.context_values.copy()
		context_values[DIR_STRUCTURE_CONTEXT_NAME] = MockDirStructure(trees_dir_items=[subdir_sha1])
		Directory(name=None, items=[item], context_values=context_values)
		
		target = item.get_target_object()
		
		self.assertIsInstance(target, MockDirStructure.Item)
