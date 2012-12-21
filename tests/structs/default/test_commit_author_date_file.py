from gitviewfs_objects import CommitPersonDateFile, CommitContextNames,\
	CommitPersonTypes
from tests.structs.default import paths
from tests.structs.default.utils import BaseDefaultDirStructTest


class CommitAuthorDateFileTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.COMMIT_AUTHOR_DATE_FILE, CommitPersonDateFile)
		self.assertEqual(CommitPersonTypes.AUTHOR, self.obj.get_context_value(CommitContextNames.PERSON_TYPE))
