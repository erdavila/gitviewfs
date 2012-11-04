import unittest
from tests.test_integration import TestIntegration
import subprocess


class TestCommitAuthorEmailFile(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


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


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()