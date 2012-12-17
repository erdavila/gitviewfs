import subprocess

from gitviewfs_objects import CommitParentSymLink, CommitContextNames, Directory,\
	DIR_STRUCTURE_CONTEXT_NAME
from tests.test_with_repository import TestWithRepository


class TestCommitParentSymLinkWithRepository(TestWithRepository):


	def test_get_target_object(self):
		self.create_and_commit_file(content='Initial version')
		initial_commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		branches = []
		NUM_PARENTS = 15
		for i in xrange(NUM_PARENTS):
			branch = 'branch%d' % i
			branches.append(branch)
			subprocess.check_call(['git', 'checkout', '-b', branch, initial_commit_sha1])
			self.create_and_commit_file(filename='file%d.txt' % i)
		
		subprocess.check_call(['git', 'checkout', branches[0]])
		subprocess.check_call(['git', 'merge'] + branches)
		
		TESTED_PARENT_NUMBER = 7
		TESTED_PARENT_INDEX = TESTED_PARENT_NUMBER - 1
		tested_parent_sha1 = subprocess.check_output(['git', 'rev-parse', branches[TESTED_PARENT_INDEX]]).strip()
		
		test = self
		FAKE_TARGET = object()
		class FakeDirStruct(object):
			def get_commits_dir(self):
				class FakeCommitsDir(object):
					def get_item(self, name):
						test.assertEqual(tested_parent_sha1, name)
						return FAKE_TARGET
				return FakeCommitsDir()
		fake_dir_struct = FakeDirStruct()
		
		commit_parent_symlink = CommitParentSymLink(name=None, parent_number=TESTED_PARENT_NUMBER)
		Directory(name=None,
				items=[commit_parent_symlink],
				context_values={
					CommitContextNames.SHA1 : 'HEAD',
					DIR_STRUCTURE_CONTEXT_NAME : fake_dir_struct,
				}
		)
		
		target = commit_parent_symlink.get_target_object()
		
		self.assertIs(FAKE_TARGET, target)
