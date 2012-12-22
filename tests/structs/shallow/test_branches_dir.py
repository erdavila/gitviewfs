import os
import subprocess

from gitviewfs_objects import BranchesProvider
from tests.structs.shallow import paths
from tests.structs.shallow.utils import BaseDefaultDirStructTest,\
	BaseDefaultDirStructIntegrationTest


class BranchesDirTest(BaseDefaultDirStructTest):
	
	def test_path(self):
		self.assertPathIsDirectoryWithProvider(paths.BRANCHES_DIR, BranchesProvider)
	

class BranchesDirIntegrationTest(BaseDefaultDirStructIntegrationTest):
	
	def test_list(self):
		self.create_and_commit_file('some content')
		self.create_and_commit_file('Another cOnTeNt')
		
		CREATED_BRANCH = 'another-branch'
		subprocess.check_output(['git', 'checkout', '-b', CREATED_BRANCH, 'HEAD~1'])
		self.create_and_commit_file('YET another CoNtEnT')
		
		branches_dir_path = self.make_branches_dir_path()
		branches = os.listdir(branches_dir_path)
		
		self.assertItemsEqual(['master', CREATED_BRANCH], branches)
