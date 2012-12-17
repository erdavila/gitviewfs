import subprocess

from gitviewfs_objects import BranchSymLink, DIR_STRUCTURE_CONTEXT_NAME
from tests.test_with_repository import TestWithRepository, MockDirStructure


class TestBranchSymLink(TestWithRepository):

	def test_target(self):
		BRANCH = 'master'
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', BRANCH]).strip()
		dir_struct = MockDirStructure(commits_dir_items=[commit_sha1])
		branch_symlink = BranchSymLink(name=BRANCH, context_values={DIR_STRUCTURE_CONTEXT_NAME:dir_struct})
		
		target = branch_symlink.get_target_object()
		
		self.assertIsInstance(target, MockDirStructure.Item)
		self.assertEqual(commit_sha1, target.name)
		self.assertEqual('commits_dir', target.source)
