import unittest
import os
import subprocess
import tempfile
import shutil

import gitviewfs
from gitviewfs_objects import RefsDir, ObjectsDir


class TestIntegration(unittest.TestCase):

	def __gitviewfs_cmd_path(self):
		main_file_path = gitviewfs.__file__
		cmd_path = self.__replace_extension(main_file_path, '.py')
		return cmd_path
	
	def __replace_extension(self, path, new_extension):
		path, _ = os.path.splitext(gitviewfs.__file__)
		path += new_extension
		return path

	def setUp(self):
		self.repo = tempfile.mkdtemp(prefix='gitviewfs-repo-', suffix='.tmp')
		self.mountpoint = tempfile.mkdtemp(prefix='gitviewfs-mountpoint-', suffix='.tmp')
		subprocess.check_call(['git', 'init', self.repo])
		subprocess.check_call([
				self.__gitviewfs_cmd_path(),
				self.mountpoint,
				'-o', 'repo=' + self.repo,
		])

	def tearDown(self):
		subprocess.check_call(['fusermount', '-u', self.mountpoint])
		shutil.rmtree(self.mountpoint)
		shutil.rmtree(self.repo)

	
	def test_list_root_dir(self):
		items = os.listdir(self.mountpoint)
		self.assertItemsEqual(['refs', 'objects', 'remotes'], items)
	
	def test_list_refs_dir(self):
		refs_dir = os.path.join(self.mountpoint, RefsDir.NAME)
		items = os.listdir(refs_dir)
		self.assertItemsEqual(['HEAD', 'branches', 'tags', 'remotes'], items)
	
	def test_list_objects_dir(self):
		refs_dir = os.path.join(self.mountpoint, ObjectsDir.NAME)
		items = os.listdir(refs_dir)
		self.assertItemsEqual(['all', 'blobs', 'commits', 'trees'], items)
	
	def test_HEAD_is_symlink(self):
		head_ref = os.path.join(self.mountpoint, RefsDir.NAME, 'HEAD')
		self.assertTrue(os.path.islink(head_ref))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_list_root_dir']
	unittest.main()
