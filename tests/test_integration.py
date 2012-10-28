import unittest
import os
import subprocess
import tempfile
import shutil

import gitviewfs
from gitviewfs_objects import RefsDir, ObjectsDir, BlobsDir, TreesDir
import stat


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
		os.chdir(self.repo)

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
	
	def test_blobs_is_directory(self):
		blobs_path = os.path.join(self.mountpoint, ObjectsDir.NAME, BlobsDir.NAME)
		self.assertTrue(os.path.isdir(blobs_path))
	
	def test_blob_content(self):
		filename, content = self._create_and_commit_file()
		sha1 = subprocess.check_output(['git', 'hash-object', filename])
		sha1 = sha1.strip()
		
		blob_path = os.path.join(self.mountpoint, ObjectsDir.NAME, BlobsDir.NAME, sha1)
		with open(blob_path) as f:
			read_content = f.read()
		
		self.assertEqual(read_content, content)
	
	def test_blob_attributes(self):
		filename, content = self._create_and_commit_file()
		sha1 = subprocess.check_output(['git', 'hash-object', filename])
		sha1 = sha1.strip()
		blob_path = os.path.join(self.mountpoint, ObjectsDir.NAME, BlobsDir.NAME, sha1)
		
		st = os.stat(blob_path)
		
		self.assertEqual(st.st_size, len(content))
		
		self.assertFalse(st.st_mode & stat.S_IXUSR)
		self.assertFalse(st.st_mode & stat.S_IXGRP)
		self.assertFalse(st.st_mode & stat.S_IXOTH)
	
	def test_blob_is_regular_file(self):
		filename, _ = self._create_and_commit_file()
		sha1 = subprocess.check_output(['git', 'hash-object', filename])
		sha1 = sha1.strip()
		
		blob_path = os.path.join(self.mountpoint, ObjectsDir.NAME, BlobsDir.NAME, sha1)
		
		self.assertTrue(os.path.isfile(blob_path))
	
	def _create_and_commit_file(self):
		content = '''This is the content
		in a Git blob file'''
		filename = 'file.txt'
		
		with open(filename, 'w') as f:
			f.write(content)
		
		subprocess.check_call(['git', 'add', filename])
		subprocess.check_call(['git', 'commit', '-m', 'Add file'])
		
		return filename, content
	
	def test_trees_dir_is_directory(self):
		trees_dir = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME)
		self.assertTrue(os.path.isdir(trees_dir))
	
	def test_tree_dir_is_directory(self):
		self._create_and_commit_file()
		sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'])
		sha1 = sha1.strip()
		
		tree_dir = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME, sha1)
		
		self.assertTrue(os.path.isdir(tree_dir))
	
	def test_tree_dir_content(self):
		filename = 'file.txt'
		with open(filename, 'w') as f:
			f.write('Some content')
		subdir = 'sub-dir'
		os.mkdir(subdir)
		with open(os.path.join(subdir, 'other-file'), 'w') as f:
			f.write('Other content')
		subprocess.check_call(['git', 'add', '.'])
		subprocess.check_call(['git', 'commit', '-m', 'Add file'])
		sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'])
		sha1 = sha1.strip()
		
		tree_dir = os.path.join(self.mountpoint, ObjectsDir.NAME, TreesDir.NAME, sha1)
		
		dir_content = os.listdir(tree_dir)
		
		self.assertItemsEqual([filename, subdir], dir_content)
	
	def test_HEAD_is_symlink(self):
		head_ref = os.path.join(self.mountpoint, RefsDir.NAME, 'HEAD')
		self.assertTrue(os.path.islink(head_ref))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_list_root_dir']
	unittest.main()
