import os.path
import shutil
import subprocess
import tempfile
import time

import gitviewfs
from tests.test_with_repository import TestWithRepository


class TestIntegrationBase(TestWithRepository):

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
