from gitviewfs_objects import HeadSymLink, BranchSymLink
from tests.test_with_repository import TestWithRepository


class TestHeadSymLink(TestWithRepository):

	def test_target(self):
		self.create_and_commit_file()
		head_sym_link = HeadSymLink(name=None)
		target_object = head_sym_link.get_target_object()
		self.assertIsInstance(target_object, BranchSymLink)
