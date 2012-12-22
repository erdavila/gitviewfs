import subprocess

from gitviewfs_objects import CommitTreeSymLink
from tests.structs.shallow import paths 
from tests.structs.shallow.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class CommitTreeSymLinkPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_TREE_SYMLINK, CommitTreeSymLink)


class CommitTreeSymLinkIntegrationTest(BaseDefaultDirStructIntegrationTest):
	
	def test_readlink(self):
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		commit_tree_symlink_path = self.make_commit_tree_symlink_path(commit_sha1)
		
		self.assertSymLink(self.make_tree_dir_path(tree_sha1), commit_tree_symlink_path)
