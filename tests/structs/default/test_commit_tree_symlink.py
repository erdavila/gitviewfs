import subprocess
import unittest

from gitviewfs_objects import get_gitviewfs_object, CommitTreeSymLink
from tests.structs.default.test_integration import TestIntegration
from tests.structs.default import paths 


class TestCommitTreeSymLink(unittest.TestCase):
	
	def test_path(self):
		commit_tree_symlink = get_gitviewfs_object(paths.COMMIT_TREE_SYMLINK)
		
		self.assertIsInstance(commit_tree_symlink, CommitTreeSymLink)
		self.assertEqual(paths.COMMIT_TREE_SYMLINK, commit_tree_symlink.get_path())


class TestCommitTreeSymLinkIntegration(TestIntegration):
	
	def test_readlink(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		commit_tree_symlink_path = self.make_commit_tree_symlink_path(commit_sha1)
		
		self.assertSymLink(self.make_tree_dir_path(tree_sha1), commit_tree_symlink_path)
