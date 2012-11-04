import unittest
from tests.test_integration import TestIntegration
import subprocess


class TestCommitCommitterNameFile(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


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


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()