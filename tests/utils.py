import os
import shutil
import subprocess
import tempfile
import unittest

from gitviewfs_objects import Directory


class BaseTest(unittest.TestCase):

	def assertIsDirectoryWithProvider(self, obj, ProviderClass):
		self.assertIsInstance(obj, Directory)
		self.assertTrue(any(isinstance(target_item, ProviderClass) for target_item in obj.items))


class BaseTestWithRepository(BaseTest):
	
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


class MockDirStructure(object):
	
	class Item(object):
		def __init__(self, name, source, **kwargs):
			self.name = name
			self.source = source
			for name, value in kwargs.iteritems():
				setattr(self, name, value)
	
	class Dir(object):
		def __init__(self, name, items_names):
			self.name = name
			self.items_names = set(items_names)
		def get_item(self, name):
			if name in self.items_names:
				return MockDirStructure.Item(name=name, source=self.name)
			else:
				raise ValueError('No item named %r in %s' % (name, self.name))
	
	class DirTemplate(object):
		def __init__(self, name):
			self.name = name
		def create_instance(self, name, **kwargs):
			return MockDirStructure.Item(
					name=name,
					source=self.name,
					kwargs=kwargs,
			)
	
	def __init__(self,
				commits_dir_items=[],
				branches_dir_items=[],
				trees_dir_items=[],
				blobs_dir_items=[]
			):
		self.__branches_dir = self.Dir('branches_dir', branches_dir_items)
		self.__commits_dir = self.Dir('commits_dir', commits_dir_items)
		self.__trees_dir = self.Dir('trees_dir', trees_dir_items)
		self.__blobs_dir = self.Dir('blobs_dir', blobs_dir_items)
		self.__commit_dir_template = self.DirTemplate('commit_dir_template')
		self.__tree_dir_template = self.DirTemplate('tree_dir_template')
	
	def get_branches_dir(self):
		return self.__branches_dir
	
	def get_commits_dir(self):
		return self.__commits_dir
	
	def get_trees_dir(self):
		return self.__trees_dir
	
	def get_blobs_dir(self):
		return self.__blobs_dir
	
	def get_commit_dir_template(self):
		return self.__commit_dir_template
	
	def get_tree_dir_template(self):
		return self.__tree_dir_template
