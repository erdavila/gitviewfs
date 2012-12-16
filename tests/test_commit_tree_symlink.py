from gitviewfs_objects import CommitTreeSymLink, CommitContextNames,\
	TreeDirItemsProvider
from tests.test_with_repository import TestWithRepository


class TestCommitTreeSymLinkWithRepository(TestWithRepository):
	
	def test_get_target_object(self):
		self.create_and_commit_file()
		symlink = CommitTreeSymLink(name=None, context_values={CommitContextNames.SHA1:'HEAD'})
		
		target = symlink.get_target_object()
		
		self.assertIsDirectoryWithProvider(target, TreeDirItemsProvider)
