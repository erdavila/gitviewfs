import subprocess
import unittest

from tests.test_integration import TestWithRepository
from gitviewfs_objects import Directory, CommitContextNames,\
	CommitParentsProvider, CommitParentSymLink


class TestCommitParentsProvider(unittest.TestCase):
	
	def test_get_item(self):
		provider = CommitParentsProvider()
		Directory(name=None, items=[provider])
		
		PARENT_NUMBER = 2
		parent_name = str(PARENT_NUMBER)
		item = provider.get_item(parent_name)
		
		self.assertIsInstance(item, CommitParentSymLink)
		self.assertEqual(item.name, parent_name)
	
	def test_get_item_with_prefix(self):
		PREFIX = 'prfx'
		provider = CommitParentsProvider(prefix=PREFIX)
		Directory(name=None, items=[provider])
		
		PARENT_NUMBER = 2
		parent_name = PREFIX + str(PARENT_NUMBER)
		item = provider.get_item(parent_name)
		
		self.assertIsInstance(item, CommitParentSymLink)
		self.assertEqual(item.name, parent_name)
		self.assertEqual(item.parent_number, PARENT_NUMBER)


class TestCommitParentsProviderWithRepository(TestWithRepository):

	def test_list_single_parent(self):
		self._test_list_parents(num_parents=1)
	
	def test_list_multiple_parents(self):
		self._test_list_parents(num_parents=3)
	
	def test_list_2_digits_parents(self):
		self._test_list_parents(num_parents=15)
	
	def test_list_3_digits_parents(self):
		self._test_list_parents(num_parents=123)
	
	def _test_list_parents(self, num_parents):
		self.create_merge_commit(num_parents)
		
		merge_commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		provider = CommitParentsProvider()
		Directory(name=None, items=[provider], context_values={CommitContextNames.SHA1:merge_commit_sha1})
		
		parents_items = provider.get_items_names()
		
		num_digits = len(str(num_parents))
		self.assertItemsEqual(['%0*d' % (num_digits, i + 1) for i in range(num_parents)], parents_items)
	
	def test_get_items_names_with_prefix(self):
		self.create_merge_commit(num_parents=12)
		merge_commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		provider = CommitParentsProvider(prefix='prfx')
		Directory(name=None, items=[provider], context_values={CommitContextNames.SHA1:merge_commit_sha1})
		
		items_names = provider.get_items_names()
		
		self.assertEqual(items_names, ['prfx01', 'prfx02', 'prfx03', 'prfx04', 'prfx05', 'prfx06', 'prfx07', 'prfx08', 'prfx09', 'prfx10', 'prfx11', 'prfx12'])
	
	def create_merge_commit(self, num_parents):
		self.create_and_commit_file(message='Initial commit')
		initial_commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		
		branches = []
		for i in xrange(num_parents):
			branch = 'branch-%d' % i
			subprocess.check_call(['git', 'checkout', '-b', branch, initial_commit_sha1])
			branches.append(branch)
			self.create_and_commit_file(filename='file%d.txt' % i)
		
		subprocess.check_call(['git', 'checkout', branches[0]])
		subprocess.check_call(['git', 'merge'] + branches)
		
		return branches


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_']
	unittest.main()
