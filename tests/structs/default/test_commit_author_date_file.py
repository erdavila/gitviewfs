import unittest

from gitviewfs_objects import get_gitviewfs_object, CommitPersonDateFile,\
	CommitPersonTypes, CommitContextNames
from tests.structs.default import paths


class TestCommitAuthorDateFile(unittest.TestCase):
	
	def test_path(self):
		commit_author_date_file = get_gitviewfs_object(paths.COMMIT_AUTHOR_DATE_FILE)
		
		self.assertIsInstance(commit_author_date_file, CommitPersonDateFile)
		self.assertEqual(CommitPersonTypes.AUTHOR, commit_author_date_file.get_context_value(CommitContextNames.PERSON_TYPE))
		self.assertEqual(paths.COMMIT_AUTHOR_DATE_FILE, commit_author_date_file.get_path())
