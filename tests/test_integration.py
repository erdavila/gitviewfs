import unittest
import os
import subprocess
import tempfile
import shutil
import time

import gitviewfs
from tests.paths import PathMaker


class TestWithRepository(unittest.TestCase):
	
	def setUp(self):
		self.repo = tempfile.mkdtemp(prefix='gitviewfs-repo-', suffix='.tmp')
		subprocess.check_call(['git', 'init', self.repo])
		os.chdir(self.repo)
	
	def tearDown(self):
		shutil.rmtree(self.repo)
	
	DEFAULT_CONTENT = '''This is the content
		in a Git blob file'''
	
	DEFAULT_MESSAGE = 'Add file'
	
	def create_and_commit_file(self, filename='file.txt', content=DEFAULT_CONTENT, message=DEFAULT_MESSAGE, author=None):
		if '/' in filename:
			directory, _ = os.path.split(filename)
			if not os.path.isdir(directory):
				os.makedirs(directory)
		with open(filename, 'w') as f:
			f.write(content)
		
		subprocess.check_call(['git', 'add', filename])
		
		commit_args = []
		if author is not None:
			commit_args.append('--author=' + author)
		
		subprocess.check_call(['git', 'commit'] + commit_args + ['-m', message])
		
		return filename, content
	
	def create_and_commit_file_and_subdir(self):
		filename = 'file.txt'
		with open(filename, 'w') as f:
			f.write('Some content')
		subdirname = 'sub-dir'
		os.mkdir(subdirname)
		with open(os.path.join(subdirname, 'other-file'), 'w') as f:
			f.write('Other content')
		subprocess.check_call(['git', 'add', '.'])
		subprocess.check_call(['git', 'commit', '-m', 'Add file'])
		
		return filename, subdirname


class TestIntegration(TestWithRepository, PathMaker):

	def __gitviewfs_cmd_path(self):
		main_file_path = gitviewfs.__file__
		cmd_path = self.__replace_extension(main_file_path, '.py')
		return cmd_path
	
	def __replace_extension(self, path, new_extension):
		path, _ = os.path.splitext(gitviewfs.__file__)
		path += new_extension
		return path

	def setUp(self):
		TestWithRepository.setUp(self)
		
		self.mountpoint = tempfile.mkdtemp(prefix='gitviewfs-mountpoint-', suffix='.tmp')
		subprocess.Popen([
				self.__gitviewfs_cmd_path(),
				self.mountpoint,
				'-d',
				'-o', 'repo=' + self.repo,
		])
		self._wait_mountpoint_available()
	
	def _wait_mountpoint_available(self):
		SLEEP_DURATION = 0.001 # in seconds
		TOTAL_WAIT_DURATION = 1 # in seconds
		for _ in xrange(int(TOTAL_WAIT_DURATION / SLEEP_DURATION)):
			time.sleep(SLEEP_DURATION)
			if os.listdir(self.mountpoint) != []:
				break
		else:
			self.fail()
	
	def tearDown(self):
		subprocess.check_call(['fusermount', '-u', self.mountpoint])
		shutil.rmtree(self.mountpoint)
		
		TestWithRepository.tearDown(self)
	
	def assertSymLink(self, expected_absolute_path, symlink_path):
		target_path = os.readlink(symlink_path)
		self.assertRelativePath(target_path)
		
		resolved_target_path = self.resolve_relative_path(symlink_path, target_path)
		self.assertEqual(expected_absolute_path, resolved_target_path)
	
	def assertRelativePath(self, path):
		self.assertFalse(os.path.isabs(path))
	
	def resolve_relative_path(self, base_file_path, relative_path):
		dir_path, _ = os.path.split(base_file_path)
		resolved_path = os.path.join(dir_path, relative_path)
		resolved_path = os.path.normpath(resolved_path)
		return resolved_path


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_list_root_dir']
	unittest.main()
