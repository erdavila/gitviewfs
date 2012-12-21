import unittest
import subprocess

from tests.utils import BaseTestWithRepository
from gitviewfs_objects import BranchesProvider, SymLink


class BranchesProviderTest(unittest.TestCase):
	
	def test_get_item(self):
		provider = BranchesProvider()
		
		NAME = 'name'
		item = provider._get_item(NAME)
		
		self.assertIsInstance(item, SymLink)
		self.assertEqual(NAME, item.name)


class BranchesProviderWithRepositoryTest(BaseTestWithRepository):

	def test_get_items_names(self):
		self.create_and_commit_file('some content')
		self.create_and_commit_file('Another cOnTeNt')
		
		CREATED_BRANCH = 'another-branch'
		subprocess.check_output(['git', 'checkout', '-b', CREATED_BRANCH, 'HEAD~1'])
		self.create_and_commit_file('YET another CoNtEnT')
		
		provider = BranchesProvider()
		
		items = provider.get_items_names()
		
		self.assertItemsEqual(['master', CREATED_BRANCH], items)
