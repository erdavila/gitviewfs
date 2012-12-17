from gitviewfs_objects import HeadSymLink, DIR_STRUCTURE_CONTEXT_NAME
from tests.test_with_repository import TestWithRepository


class TestHeadSymLink(TestWithRepository):

	def test_target(self):
		self.create_and_commit_file()
		FAKE_TARGET = object()
		class FakeDirStructure(object):
			def get_branches_dir(self):
				class FakeBranchesDir(object):
					def get_item(self, name):
						return FAKE_TARGET
				return FakeBranchesDir()
		dir_struct = FakeDirStructure()
		head_sym_link = HeadSymLink(name=None, context_values={DIR_STRUCTURE_CONTEXT_NAME:dir_struct})
		
		target_object = head_sym_link.get_target_object()
		
		self.assertIs(FAKE_TARGET, target_object)
