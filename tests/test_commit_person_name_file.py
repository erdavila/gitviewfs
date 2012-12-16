from gitviewfs_objects import CommitPersonNameFile, CommitContextNames,\
	CommitPersonTypes
from tests.test_with_repository import TestWithRepository
import subprocess


class TestCommitPersonNameFileWithRepository(TestWithRepository):

	def test_get_content_author(self):
		AUTHOR_NAME = 'Author Name'
		AUTHOR_EMAIL = 'author@email.com'
		self.create_and_commit_file(author='%s <%s>' % (AUTHOR_NAME, AUTHOR_EMAIL))
		context_values = {
			CommitContextNames.PERSON_TYPE : CommitPersonTypes.AUTHOR,
			CommitContextNames.SHA1        : 'HEAD',
		}
		name_file = CommitPersonNameFile(name=None, context_values=context_values)
		
		content = name_file.get_content()
		
		self.assertEqual(AUTHOR_NAME + '\n', content)

	def test_get_content_committer(self):
		COMMITTER_NAME = 'The Committer'
		AUTHOR = 'An Author <an@author.com>'
		subprocess.check_call(['git', 'config', 'user.name', COMMITTER_NAME])
		self.create_and_commit_file(author=AUTHOR)
		context_values = {
			CommitContextNames.PERSON_TYPE : CommitPersonTypes.COMMITTER,
			CommitContextNames.SHA1        : 'HEAD',
		}
		name_file = CommitPersonNameFile(name=None, context_values=context_values)
		
		content = name_file.get_content()
		
		self.assertEqual(COMMITTER_NAME + '\n', content)
