import subprocess
import unittest

from gitviewfs_objects import get_gitviewfs_object, CommitParentSymLink
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration


class TestCommitParentSymlink(unittest.TestCase):

	def test_path(self):
		commit_parent_symlink = get_gitviewfs_object(paths.COMMIT_PARENT_SYMLINK)
		
		self.assertIsInstance(commit_parent_symlink, CommitParentSymLink)
		self.assertEqual(paths.COMMIT_PARENT_SYMLINK, commit_parent_symlink.get_path())


class TestCommitParentSymlinkIntegration(TestIntegration):

	def test_symlink(self):
		self.create_and_commit_file(content='Version 1')
		parent_commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		self.create_and_commit_file(content='Version 2')
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		parent_commit_dir_path = self.make_commit_dir_path(parent_commit_sha1)
		parent_commit_symlink_path = self.make_commit_parent_symlink_path(commit_sha1)
		
		self.assertSymLink(parent_commit_dir_path, parent_commit_symlink_path)


	def test_not_first_parent(self):
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
		
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		tested_parent_sha1 = subprocess.check_output(['git', 'rev-parse', branches[TESTED_PARENT_INDEX]]).strip()
		
		num_digits = len(str(NUM_PARENTS))
		parent = '%0*d' % (num_digits, TESTED_PARENT_NUMBER)
		
		parent_commit_symlink_path = self.make_commit_parent_symlink_path(commit_sha1, parent)
		parent_commit_dir_path = self.make_commit_dir_path(tested_parent_sha1)
		
		self.assertSymLink(parent_commit_dir_path, parent_commit_symlink_path)
