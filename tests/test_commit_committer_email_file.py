import unittest
from tests.test_integration import TestIntegration
import subprocess


class TestCommitCommitterEmailFile(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


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


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
