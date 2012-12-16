import unittest

from gitviewfs_objects import HeadSymLink, get_gitviewfs_object
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration


class TestHeadSymLink(unittest.TestCase):
	
	def test_path(self):
		head_symlink = get_gitviewfs_object(paths.HEAD_SYMLINK)
		
		self.assertIsInstance(head_symlink, HeadSymLink)
		self.assertEqual(paths.HEAD_SYMLINK, head_symlink.get_path())


class TestHeadSymLinkIntegration(TestIntegration):
	
	def test_target(self):
		self.create_and_commit_file()
		symlink_path = self.make_head_symlink_path()
		expected_absolute_path = self.make_branch_symlink_path('master')
		
		self.assertSymLink(expected_absolute_path, symlink_path)
