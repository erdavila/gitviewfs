from gitviewfs_objects import CommitTreeSymLink, CommitContextNames,\
	DIR_STRUCTURE_CONTEXT_NAME
from tests.test_with_repository import TestWithRepository, MockDirStructure
import subprocess


class TestCommitTreeSymLinkWithRepository(TestWithRepository):
	
	def test_get_target_object(self):
		self.create_and_commit_file()
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).strip()
		
		dir_struct = MockDirStructure(trees_dir_items=[tree_sha1])
		symlink = CommitTreeSymLink(
				name=None,
				context_values={
					CommitContextNames.SHA1    : 'HEAD',
					DIR_STRUCTURE_CONTEXT_NAME : dir_struct,
				}
		)
		
		target = symlink.get_target_object()
		
		self.assertIsInstance(target, MockDirStructure.Item)
