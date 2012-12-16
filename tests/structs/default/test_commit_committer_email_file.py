import subprocess
import unittest

from gitviewfs_objects import CommitPersonEmailFile, CommitContextNames,\
	CommitPersonTypes, get_gitviewfs_object
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration


class TestCommitCommitterEmailFile(unittest.TestCase):
	
	def test_path(self):
		commit_committer_email_file = get_gitviewfs_object(paths.COMMIT_COMMITTER_EMAIL_FILE)
		
		self.assertIsInstance(commit_committer_email_file, CommitPersonEmailFile)
		self.assertEqual(CommitPersonTypes.COMMITTER, commit_committer_email_file.get_context_value(CommitContextNames.PERSON_TYPE))
		self.assertEqual(paths.COMMIT_COMMITTER_EMAIL_FILE, commit_committer_email_file.get_path())


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
