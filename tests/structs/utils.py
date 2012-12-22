from abc import ABCMeta, abstractmethod
import os.path
import shutil
import subprocess
import tempfile
import time

import gitviewfs
from tests.utils import BaseTestWithRepository, BaseTest


class BaseDirStructTest(BaseTest):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def _get_dir_structure(self):
		raise NotImplemented()
	
	def assertPathIs(self, path, Class):
		self.__assertPath(path)
		self.assertIsInstance(self.obj, Class)
	
	def assertPathIsDirectoryWithProvider(self, path, ProviderClass):
		self.__assertPath(path)
		self.assertIsDirectoryWithProvider(self.obj, ProviderClass)
	
	def __assertPath(self, path):
		dir_struct = self._get_dir_structure()
		self.obj = dir_struct.get_object(path)
		self.assertEqual(path, self.obj.get_path())


class BaseIntegrationTest(BaseTestWithRepository):
	__metaclass__ = ABCMeta

	def __gitviewfs_cmd_path(self):
		main_file_path = gitviewfs.__file__
		cmd_path = self.__replace_extension(main_file_path, '.py')
		return cmd_path
	
	def __replace_extension(self, path, new_extension):
		path, _ = os.path.splitext(gitviewfs.__file__)
		path += new_extension
		return path

	def setUp(self):
		BaseTestWithRepository.setUp(self)
		
		self.mountpoint = tempfile.mkdtemp(prefix='gitviewfs-mountpoint-', suffix='.tmp')
		subprocess.Popen([
				self.__gitviewfs_cmd_path(),
				self.mountpoint,
				'-d',
				'-o', 'repo=' + self.repo,
				'-o', 'struct=' + self.get_dir_struct_name()
		])
		self._wait_mountpoint_available()
	
	@abstractmethod
	def get_dir_struct_name(self):
		raise NotImplementedError()
	
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
		
		BaseTestWithRepository.tearDown(self)
	
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
