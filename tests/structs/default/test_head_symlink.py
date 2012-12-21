from gitviewfs_objects import HeadSymLink
from tests.structs.default import paths
from tests.structs.default.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class HeadSymLinkPathTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIs(paths.HEAD_SYMLINK, HeadSymLink)


class HeadSymLinkIntegrationTest(BaseDefaultDirStructIntegrationTest):
	
	def test_target(self):
		self.create_and_commit_file()
		symlink_path = self.make_head_symlink_path()
		expected_absolute_path = self.make_branch_symlink_path('master')
		
		self.assertSymLink(expected_absolute_path, symlink_path)
