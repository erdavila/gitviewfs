import subprocess
import unittest

from gitviewfs_objects import CommitContextNames, CommitPersonTypes,\
	CommitPersonNameFile, get_gitviewfs_object
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration


class TestCommitCommitterNameFile(unittest.TestCase):
	
	def test_path(self):
		commit_committer_email_file = get_gitviewfs_object(paths.COMMIT_COMMITTER_NAME_FILE)
		
		self.assertIsInstance(commit_committer_email_file, CommitPersonNameFile)
		self.assertEqual(CommitPersonTypes.COMMITTER, commit_committer_email_file.get_context_value(CommitContextNames.PERSON_TYPE))
		self.assertEqual(paths.COMMIT_COMMITTER_NAME_FILE, commit_committer_email_file.get_path())


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
