from gitviewfs_objects import HeadSymLink, DIR_STRUCTURE_CONTEXT_NAME
from tests.utils import BaseTestWithRepository, MockDirStructure


class HeadSymLinkTest(BaseTestWithRepository):

	def test_target(self):
		self.create_and_commit_file()
		dir_struct = MockDirStructure(branches_dir_items=['master'])
		head_sym_link = HeadSymLink(name=None, context_values={DIR_STRUCTURE_CONTEXT_NAME:dir_struct})
		
		target_object = head_sym_link.get_target_object()
		
		self.assertIsInstance(target_object, MockDirStructure.Item)
		self.assertEqual('master', target_object.name)
		self.assertEqual('branches_dir', target_object.source)
