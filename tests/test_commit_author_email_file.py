import unittest
import subprocess

from tests.test_integration import TestIntegration, TestWithRepository
from gitviewfs_objects import CommitContextNames, CommitPersonTypes,\
	CommitPersonEmailFile


class TestCommitAuthorEmailFileWithRepository(TestWithRepository):

	def test_get_content(self):
		AUTHOR_NAME = 'Author Name'
		AUTHOR_EMAIL = 'author@email.com'
		self.create_and_commit_file(author='%s <%s>' % (AUTHOR_NAME, AUTHOR_EMAIL))
		context_values = {
			CommitContextNames.PERSON_TYPE : CommitPersonTypes.AUTHOR,
			CommitContextNames.SHA1        : 'HEAD',
		}
		name_file = CommitPersonEmailFile(name=None, context_values=context_values)
		
		content = name_file.get_content()
		
		self.assertEqual(content, AUTHOR_EMAIL + '\n')


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