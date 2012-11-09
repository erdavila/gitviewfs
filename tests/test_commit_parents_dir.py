import subprocess
import unittest

from tests.test_integration import TestIntegration
import os


class TestCommitParentsDir(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass


class TestCommitParentsDirIntegration(TestIntegration):

	def test_list_single_parent(self):
		self._test_list_parents(num_parents=1)
	
	def test_list_multiple_parents(self):
		self._test_list_parents(num_parents=3)
	
	def test_list_2_digits_parents(self):
		self._test_list_parents(num_parents=15)
	
	def test_list_3_digits_parents(self):
		self._test_list_parents(num_parents=123)
	
	def _test_list_parents(self, num_parents):
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
		
		merge_commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		merge_commit_parents_dir_path = self.make_commit_parents_dir_path(merge_commit_sha1)
		
		parents_items = os.listdir(merge_commit_parents_dir_path)
		
		num_digits = len(str(num_parents))
		self.assertItemsEqual(['%0*d' % (num_digits, i + 1) for i in range(num_parents)], parents_items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_']
	unittest.main()
