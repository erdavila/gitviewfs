import subprocess

from gitviewfs_objects import BranchSymLink
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration, DefaultDirStructPathTest


class TestBranchSymLink(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.BRANCH_SYMLINK, BranchSymLink)


class TestBranchSymLinkIntegration(TestIntegration):

	def test_target(self):
		BRANCH = 'master'
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', BRANCH]).strip()
		branch_symlink_path = self.make_branch_symlink_path(BRANCH)
		
		self.assertSymLink(self.make_commit_dir_path(commit_sha1), branch_symlink_path)
