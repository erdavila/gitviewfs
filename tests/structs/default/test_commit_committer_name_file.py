import subprocess

from gitviewfs_objects import CommitContextNames, CommitPersonTypes,\
	CommitPersonNameFile
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class CommitCommitterNameFilePathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_COMMITTER_NAME_FILE, CommitPersonNameFile)
		self.assertEqual(CommitPersonTypes.COMMITTER, self.obj.get_context_value(CommitContextNames.PERSON_TYPE))


class TestCommitCommitterNameFileIntegration(TestIntegration):
	
	def test_content(self):
		COMMITTER_NAME = 'The Committer'
		AUTHOR = 'An Author <an@author.com>'
		subprocess.check_call(['git', 'config', 'user.name', COMMITTER_NAME])
		self.create_and_commit_file(author=AUTHOR)
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		commit_committer_name_file_path = self.make_commit_committer_name_file_path(commit_sha1)
		
		with open(commit_committer_name_file_path) as f:
			commit_committer_name = f.read()
		
		self.assertEqual(COMMITTER_NAME + '\n', commit_committer_name)
