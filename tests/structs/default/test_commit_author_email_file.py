import subprocess
import unittest

from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration
from gitviewfs_objects import CommitPersonEmailFile, CommitContextNames,\
	get_gitviewfs_object, CommitPersonTypes


class TestCommitAuthorEmailFile(unittest.TestCase):
	
	def test_path(self):
		commit_author_email_file = get_gitviewfs_object(paths.COMMIT_AUTHOR_EMAIL_FILE)
		
		self.assertIsInstance(commit_author_email_file, CommitPersonEmailFile)
		self.assertEqual(CommitPersonTypes.AUTHOR, commit_author_email_file.get_context_value(CommitContextNames.PERSON_TYPE))
		self.assertEqual(paths.COMMIT_AUTHOR_EMAIL_FILE, commit_author_email_file.get_path())


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
