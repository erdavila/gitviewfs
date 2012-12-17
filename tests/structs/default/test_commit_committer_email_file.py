import subprocess

from gitviewfs_objects import CommitPersonEmailFile, CommitContextNames,\
	CommitPersonTypes
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class CommitCommitterEmailFilePathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_COMMITTER_EMAIL_FILE, CommitPersonEmailFile)
		self.assertEqual(CommitPersonTypes.COMMITTER, self.obj.get_context_value(CommitContextNames.PERSON_TYPE))


class TestCommitCommitterEmailFileIntegration(TestIntegration):
	
	def test_content(self):
		COMMITTER_EMAIL = 'committer@yes.net'
		AUTHOR = 'An Author <an@author.com>'
		subprocess.check_call(['git', 'config', 'user.email', COMMITTER_EMAIL])
		self.create_and_commit_file(author=AUTHOR)
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		commit_committer_email_file_path = self.make_commit_committer_email_file_path(commit_sha1)
		
		with open(commit_committer_email_file_path) as f:
			commit_committer_email = f.read()
		
		self.assertEqual(COMMITTER_EMAIL + '\n', commit_committer_email)
