import subprocess

from gitviewfs_objects import CommitPersonNameFile, CommitContextNames,\
	CommitPersonTypes
from tests.structs.default import paths
from tests.structs.default.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class CommitAuthorNameFilePathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_AUTHOR_NAME_FILE, CommitPersonNameFile)
		self.assertEqual(CommitPersonTypes.AUTHOR, self.obj.get_context_value(CommitContextNames.PERSON_TYPE))


class CommitAuthorNameFileIntegrationTest(BaseDefaultDirStructIntegrationTest):
	
	def test_content(self):
		AUTHOR_NAME = 'The Name'
		subprocess.check_call(['git', 'config', 'user.name', AUTHOR_NAME])
		self.create_and_commit_file()
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		commit_author_name_file_path = self.make_commit_author_name_file_path(commit_sha1)
		
		with open(commit_author_name_file_path) as f:
			commit_author_name = f.read()
		
		self.assertEqual(AUTHOR_NAME + '\n', commit_author_name)
