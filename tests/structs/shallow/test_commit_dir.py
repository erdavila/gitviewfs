import os
import subprocess

from gitviewfs_objects import Directory, CommitContextNames
import dir_structure.shallow
from tests.structs.shallow import paths
from tests.structs.shallow.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest
from tests.utils import BaseTestWithRepository


class CommitDirPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_DIR, Directory)


class CommitDirTest(BaseTestWithRepository):
	
	def test_get_items_names(self):
		self.create_and_commit_file(content='parent commit')
		self.create_and_commit_file(content='current commit')
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		dir_struct = dir_structure.shallow.Shallow()
		commit_dir_template = dir_struct.get_commit_dir_template()
		commit_dir = commit_dir_template.create_instance(name=commit_sha1, context_values={CommitContextNames.SHA1:commit_sha1})
		
		items = commit_dir.get_items_names()
		
		self.assertItemsEqual(
			[
				'message',
				'author-name'   , 'author-email'   , 'author-date',
				'committer-name', 'committer-email', 'committer-date',
				'parent1', 'tree',
			],
			items
		)


class CommitDirIntegrationTest(BaseDefaultDirStructIntegrationTest):
	
	def test_is_directory(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		commit_dir_path = self.make_commit_dir_path(commit_sha1)
		
		self.assertTrue(os.path.isdir(commit_dir_path))
