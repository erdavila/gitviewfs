import subprocess

from gitviewfs_objects import BranchSymLink, Directory,\
	DIR_STRUCTURE_CONTEXT_NAME
from tests.test_with_repository import TestWithRepository


class TestBranchSymLink(TestWithRepository):

	def test_target(self):
		test = self
		
		BRANCH = 'master'
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', BRANCH]).strip()
		FAKE_TARGET = object()
		class FakeDirStruct(object):
			def get_commits_dir(self):
				class FakeCommitsDir(object):
					def get_item(self, name):
						test.assertEqual(commit_sha1, name)
						return FAKE_TARGET
				return FakeCommitsDir()
		fake_dir_struct = FakeDirStruct()
		branch_symlink = BranchSymLink(name=BRANCH, context_values={DIR_STRUCTURE_CONTEXT_NAME:fake_dir_struct})
		
		target = branch_symlink.get_target_object()
		
		self.assertIs(FAKE_TARGET, target)
