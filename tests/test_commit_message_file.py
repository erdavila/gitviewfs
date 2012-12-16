import subprocess

from tests.test_with_repository import TestWithRepository
from gitviewfs_objects import CommitMessageFile, CommitContextNames, Directory


class TestCommitMessageFileWithRepository(TestWithRepository):
	
	def test_content(self):
		MESSAGE = 'This is a commit message'
		self.create_and_commit_file(message=MESSAGE)
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		commit_message_file = CommitMessageFile(name=None)
		Directory(name=None, items=[commit_message_file], context_values={CommitContextNames.SHA1:commit_sha1})
		
		content = commit_message_file.get_content()
		self.assertEqual(MESSAGE + '\n', content)
