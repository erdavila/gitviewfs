import unittest

from gitviewfs_objects import get_gitviewfs_object, CommitPersonDateFile, \
	CommitPersonTypes, CommitContextNames
from tests.structs.default import paths


class TestCommitCommitterDateFile(unittest.TestCase):
	
	def test_path(self):
		commit_committer_date_file = get_gitviewfs_object(paths.COMMIT_COMMITTER_DATE_FILE)
		
		self.assertIsInstance(commit_committer_date_file, CommitPersonDateFile)
		self.assertEqual(CommitPersonTypes.COMMITTER, commit_committer_date_file.get_context_value(CommitContextNames.PERSON_TYPE))
		self.assertEqual(paths.COMMIT_COMMITTER_DATE_FILE, commit_committer_date_file.get_path())
