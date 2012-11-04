import unittest
from tests.test_integration import TestIntegration
import subprocess


class TestCommitAuthorNameFile(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


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


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()