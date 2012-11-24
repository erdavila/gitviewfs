import unittest
import subprocess

from gitviewfs_objects import CommitPersonNameFile, CommitContextNames,\
	CommitPersonTypes
from tests.test_integration import TestIntegration, TestWithRepository


class TestCommitAuthorNameFileWithRepository(TestWithRepository):

	def test_get_content(self):
		AUTHOR_NAME = 'Author Name'
		AUTHOR_EMAIL = 'author@email.com'
		self.create_and_commit_file(author='%s <%s>' % (AUTHOR_NAME, AUTHOR_EMAIL))
		context_values = {
			CommitContextNames.PERSON_TYPE : CommitPersonTypes.AUTHOR,
			CommitContextNames.SHA1        : 'HEAD',
		}
		name_file = CommitPersonNameFile(name='author', context_values=context_values)
		
		content = name_file.get_content()
		
		self.assertEqual(content, AUTHOR_NAME + '\n')


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
