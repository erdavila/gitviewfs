import unittest

from gitviewfs_objects import GitViewFSObject, Directory


class GitViewFSObjectTest(unittest.TestCase):

	def test_context_values(self):
		NAME1 = 'name1'
		NAME2 = 'name2'
		VALUE1 = 'value1'
		VALUE2 = 'value2'
		context_values = {
			NAME1 : VALUE1,
			NAME2 : VALUE2,
		}
		obj = GitViewFSObject(context_values=context_values, name=None)
		
		self.assertEqual(obj.get_context_value(NAME1), VALUE1)
		self.assertEqual(obj.get_context_value(NAME2), VALUE2)
	
	def test_context_values_from_parent_dir(self):
		NAME = 'name'
		VALUE = 'value'
		obj = GitViewFSObject(name=None)
		parent_dir = Directory(context_values={NAME:VALUE}, name=None, items=[obj])
		_ = parent_dir
		
		value = obj.get_context_value(NAME)
		
		self.assertEqual(value, VALUE)
