import subprocess
import unittest

from gitviewfs_objects import get_gitviewfs_object, BranchSymLink
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration


class TestBranchSymLink(unittest.TestCase):
	
	def test_path(self):
		branch_symlink = get_gitviewfs_object(paths.BRANCH_SYMLINK)
		
		self.assertIsInstance(branch_symlink, BranchSymLink)
		self.assertEqual(paths.BRANCH_SYMLINK, branch_symlink.get_path())

class TestBranchSymLinkIntegration(TestIntegration):

	def test_target(self):
		BRANCH = 'master'
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', BRANCH]).strip()
		branch_symlink_path = self.make_branch_symlink_path(BRANCH)
		
		self.assertSymLink(self.make_commit_dir_path(commit_sha1), branch_symlink_path)
