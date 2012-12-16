import os

from gitviewfs_objects import get_gitviewfs_object, CommitsProvider
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration
from tests.test_with_repository import TestBase


class TestCommitsDir(TestBase):

	def test_path(self):
		commits_dir = get_gitviewfs_object(paths.COMMITS_DIR)
		
		self.assertIsDirectoryWithProvider(commits_dir, CommitsProvider)
		self.assertEqual(paths.COMMITS_DIR, commits_dir.get_path())


class TestCommitsDirIntegration(TestIntegration):

	def test_list(self):
		commits_dir_path = self.make_commits_dir_path()
		
		items = os.listdir(commits_dir_path)
		
		self.assertItemsEqual([], items)
