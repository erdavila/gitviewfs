import subprocess

from gitviewfs_objects import CommitPersonEmailFile, CommitContextNames,\
	CommitPersonTypes
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class CommitAuthorEmailFilePathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_AUTHOR_EMAIL_FILE, CommitPersonEmailFile)
		self.assertEqual(CommitPersonTypes.AUTHOR, self.obj.get_context_value(CommitContextNames.PERSON_TYPE))


class TestCommitAuthorEmailFileIntegration(TestIntegration):
	
	def test_content(self):
		AUTHOR_EMAIL = 'abc@xyz.com'
		subprocess.check_call(['git', 'config', 'user.email', AUTHOR_EMAIL])
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		commit_author_email_file_path = self.make_commit_author_email_file_path(commit_sha1)
		
		with open(commit_author_email_file_path) as f:
			commit_author_email = f.read()
		
		self.assertEqual(AUTHOR_EMAIL + '\n', commit_author_email)
