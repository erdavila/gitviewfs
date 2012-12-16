import subprocess
import unittest

from gitviewfs_objects import get_gitviewfs_object, CommitContextNames,\
	CommitPersonTypes, CommitPersonNameFile
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration


class TestCommitAuthorNameFile(unittest.TestCase):
	
	def test_path(self):
		commit_author_email_file = get_gitviewfs_object(paths.COMMIT_AUTHOR_NAME_FILE)
		
		self.assertIsInstance(commit_author_email_file, CommitPersonNameFile)
		self.assertEqual(CommitPersonTypes.AUTHOR, commit_author_email_file.get_context_value(CommitContextNames.PERSON_TYPE))
		self.assertEqual(paths.COMMIT_AUTHOR_NAME_FILE, commit_author_email_file.get_path())


class TestCommitAuthorNameFileIntegration(TestIntegration):
	
	def test_content(self):
		AUTHOR_NAME = 'The Name'
		subprocess.check_call(['git', 'config', 'user.name', AUTHOR_NAME])
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		commit_author_name_file_path = self.make_commit_author_name_file_path(commit_sha1)
		
		with open(commit_author_name_file_path) as f:
			commit_author_name = f.read()
		
		self.assertEqual(AUTHOR_NAME + '\n', commit_author_name)
