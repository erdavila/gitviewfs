import subprocess
import unittest

from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration
from gitviewfs_objects import get_gitviewfs_object, CommitMessageFile


class TestCommitMessageFile(unittest.TestCase):
	
	def test_path(self):
		commit_message_file = get_gitviewfs_object(paths.COMMIT_MESSAGE_FILE)
		
		self.assertIsInstance(commit_message_file, CommitMessageFile)
		self.assertEqual(paths.COMMIT_MESSAGE_FILE, commit_message_file.get_path())


class TestCommitMessageFileIntegration(TestIntegration):
	
	def test_content(self):
		self.message = '''
			This is a
			multiline
			commit message
		'''.strip() + '\n'
		self.create_and_commit_file(message=self.message)
		self.commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		self.commit_message_path = self.make_commit_message_file_path(self.commit_sha1)
	
		with open(self.commit_message_path) as f:
			content = f.read()
		
		self.assertEqual(self.message, content)
