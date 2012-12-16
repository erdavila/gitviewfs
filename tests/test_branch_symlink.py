import subprocess

from gitviewfs_objects import BranchSymLink, Directory
from tests.test_with_repository import TestWithRepository


class TestBranchSymLink(TestWithRepository):

	def test_target(self):
		BRANCH = 'master'
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', BRANCH]).strip()
		branch_symlink = BranchSymLink(name=BRANCH)
		
		target = branch_symlink.get_target_object()
		
		self.assertIsInstance(target, Directory)
		self.assertEqual(commit_sha1, target.name)
