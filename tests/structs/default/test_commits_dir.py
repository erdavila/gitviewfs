import os

from gitviewfs_objects import CommitsProvider
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class CommitsDirPathTest(DefaultDirStructPathTest):

	def test_path(self):
		self.assertPathIsDirectoryWithProvider(paths.COMMITS_DIR, CommitsProvider)


class TestCommitsDirIntegration(TestIntegration):

	def test_list(self):
		commits_dir_path = self.make_commits_dir_path()
		
		items = os.listdir(commits_dir_path)
		
		self.assertItemsEqual([], items)
