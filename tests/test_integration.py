import unittest
import os
import subprocess
import tempfile
import shutil

import gitviewfs


class Test(unittest.TestCase):

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
				'-o', 'root=' + self.repo,
		])

	def tearDown(self):
		subprocess.check_call(['fusermount', '-u', self.mountpoint])
		shutil.rmtree(self.mountpoint)
		shutil.rmtree(self.repo)

	
	def test_list_root_dir(self):
		items = os.listdir(self.mountpoint)
		self.assertItemsEqual(['refs', 'objects', 'remotes'], items)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_list_root_dir']
	unittest.main()
