from gitviewfs_objects import CommitPersonDateFile, CommitContextNames,\
	CommitPersonTypes
from tests.structs.shallow import paths
from tests.structs.shallow.utils import BaseDefaultDirStructTest


class CommitCommitterDateFilePathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_COMMITTER_DATE_FILE, CommitPersonDateFile)
		self.assertEqual(CommitPersonTypes.COMMITTER, self.obj.get_context_value(CommitContextNames.PERSON_TYPE))
