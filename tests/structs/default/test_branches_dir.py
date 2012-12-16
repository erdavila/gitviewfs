import os
import subprocess

from gitviewfs_objects import get_gitviewfs_object, BranchesProvider
from tests.structs.default import paths
from tests.structs.default.test_integration import TestIntegration
from tests.test_with_repository import TestBase


class TestBranchesDir(TestBase):
	
	def test_path(self):
		branches_dir = get_gitviewfs_object(paths.BRANCHES_DIR)
		
		self.assertIsDirectoryWithProvider(branches_dir, BranchesProvider)
		self.assertEqual(paths.BRANCHES_DIR, branches_dir.get_path())
	

class TestBranchesDirIntegration(TestIntegration):
	
	def test_list(self):
		self.create_and_commit_file('some content')
		self.create_and_commit_file('Another cOnTeNt')
		
		CREATED_BRANCH = 'another-branch'
		subprocess.check_output(['git', 'checkout', '-b', CREATED_BRANCH, 'HEAD~1'])
		self.create_and_commit_file('YET another CoNtEnT')
		
		branches_dir_path = self.make_branches_dir_path()
		branches = os.listdir(branches_dir_path)
		
		self.assertItemsEqual(['master', CREATED_BRANCH], branches)
