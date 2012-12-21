import os

from gitviewfs_objects import CommitsProvider
from tests.structs.default import paths
from tests.structs.default.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class CommitsDirPathTest(BaseDefaultDirStructTest):

	def test_path(self):
		self.assertPathIsDirectoryWithProvider(paths.COMMITS_DIR, CommitsProvider)


class CommitsDirIntegrationTest(BaseDefaultDirStructIntegrationTest):

	def test_list(self):
		commits_dir_path = self.make_commits_dir_path()
		
		items = os.listdir(commits_dir_path)
		
		self.assertItemsEqual([], items)
