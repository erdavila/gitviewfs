import os
import shutil
import subprocess
import tempfile
import unittest

from gitviewfs_objects import Directory


class TestBase(unittest.TestCase):

	def assertIsDirectoryWithProvider(self, obj, ProviderClass):
		self.assertIsInstance(obj, Directory)
		self.assertTrue(any(isinstance(target_item, ProviderClass) for target_item in obj.items))


class TestWithRepository(TestBase):
	
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
