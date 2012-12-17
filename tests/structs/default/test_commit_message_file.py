import subprocess

from gitviewfs_objects import CommitMessageFile
from tests.structs.default import paths
from tests.structs.default.utils import TestIntegration,\
	DefaultDirStructPathTest


class CommitMessageFilePathTest(DefaultDirStructPathTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_MESSAGE_FILE, CommitMessageFile)


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
