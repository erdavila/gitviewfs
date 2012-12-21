import subprocess

from tests.utils import BaseTestWithRepository, MockDirStructure
from gitviewfs_objects import Directory, TreeContextNames, TreeDirItem,\
	DIR_STRUCTURE_CONTEXT_NAME
from git_objects_parser import GitTreeParser


class TreeDirItemWithRepositoryTest(BaseTestWithRepository):

	def setUp(self):
		super(TreeDirItemWithRepositoryTest, self).setUp()
		self.filename, self.subdirname = self.create_and_commit_file_and_subdir()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		self.context_values = {TreeContextNames.SHA1:tree_sha1}
		
		parser = GitTreeParser()
		self.tree_items = parser.parse('HEAD^{tree}')
	
	def test_file_as_blob(self):
		file_sha1 = self.tree_items[self.filename].sha1
		
		context_values = self.context_values.copy()
		context_values[DIR_STRUCTURE_CONTEXT_NAME] = MockDirStructure(blobs_dir_items=[file_sha1])
		
		item = TreeDirItem(name=self.filename)
		Directory(name=None, items=[item], context_values=context_values)
		
		target = item.get_target_object()
		
		self.assertIsInstance(target, MockDirStructure.Item)
	
	def test_subdir_as_tree(self):
		subdir_sha1 = self.tree_items[self.subdirname].sha1
		
		context_values = self.context_values.copy()
		context_values[DIR_STRUCTURE_CONTEXT_NAME] = MockDirStructure(trees_dir_items=[subdir_sha1])
		
		item = TreeDirItem(name=self.subdirname)
		Directory(name=None, items=[item], context_values=context_values)
		
		target = item.get_target_object()
		
		self.assertIsInstance(target, MockDirStructure.Item)
