import stat
import posix
import os
import subprocess


REMOTES_DIR = 'remotes'


def without_write_permissions(stat_mode):
	stat_mode &= ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
	return stat_mode

def without_execution_permissions(stat_mode):
	stat_mode &= ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
	return stat_mode

def with_symlink_file_type(stat_mode):
	stat_mode = with_clear_file_type(stat_mode)
	stat_mode |= stat.S_IFLNK
	return stat_mode

def with_regular_file_type(stat_mode):
	stat_mode = with_clear_file_type(stat_mode)
	stat_mode |= stat.S_IFREG
	return stat_mode

def with_clear_file_type(stat_mode):
	stat_mode ^= stat.S_IFMT(stat_mode)
	return stat_mode


def create_gitviewfs_object(path):
	assert path.startswith('/')
	
	path_parts = path.split('/')
	root_dir = RootDir()
	
	obj = root_dir.create_gitviewfs_object(path_parts[1:])
	return obj


class GitViewFSObject(object):
	
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
	
	
	def getattr(self):
		st_root = os.lstat('.')
		
		attrs = list(st_root)
		attrs[stat.ST_MODE] = without_write_permissions(attrs[stat.ST_MODE])
		attrs[stat.ST_NLINK] = 1
		
		return posix.stat_result(attrs)
	
	def _is_valid_sha1_hash(self, sha1_hash):
		return 4 <= len(sha1_hash) <= 40


class RootDir(GitViewFSObject):
	
	PATH = '/'
	
	def __init__(self):
		super(RootDir, self).__init__(parent=None, name='/')
	
	def create_gitviewfs_object(self, path_parts):
		if path_parts == ['']:
			return self
		
		first_part = path_parts[0]
		
		if first_part == RefsDir.NAME:
			refs_dir = RefsDir(parent=self, name=first_part)
			return refs_dir.create_gitviewfs_object(path_parts[1:])
		
		if first_part == ObjectsDir.NAME:
			objects_dir = ObjectsDir(parent=self, name=first_part)
			return objects_dir.create_gitviewfs_object(path_parts[1:])
	
	def list(self):
		return [RefsDir.NAME, ObjectsDir.NAME, REMOTES_DIR]


class RefsDir(GitViewFSObject):
	
	NAME = 'refs'
	
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
	
	def create_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		if path_parts == ['HEAD']:
			head_symlink = HeadSymLink(parent=self)
			return head_symlink
	
	def list(self):
		return ['HEAD', 'branches', 'tags', 'remotes']


class HeadSymLink(GitViewFSObject):
	
	def __init__(self, parent):
		self.parent = parent
	
	def getattr(self):
		stat_result = super(HeadSymLink, self).getattr()
		
		attrs = list(stat_result)
		attrs[stat.ST_MODE] = with_symlink_file_type(attrs[stat.ST_MODE])
		return posix.stat_result(attrs)


class ObjectsDir(GitViewFSObject):
	
	NAME = 'objects'
	
	def create_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		first_part = path_parts[0]
		
		if first_part == BlobsDir.NAME:
			blobs_dir = BlobsDir(parent=self, name=first_part)
			return blobs_dir.create_gitviewfs_object(path_parts[1:])
		
		if first_part == TreesDir.NAME:
			trees_dir = TreesDir(parent=self, name=first_part)
			return trees_dir.create_gitviewfs_object(path_parts[1:])
	
	
	def list(self):
		return ['commits', TreesDir.NAME, BlobsDir.NAME, 'all']


class TreesDir(GitViewFSObject):
	
	NAME = 'trees'
	
	def create_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		first_part = path_parts[0]
		if self._is_valid_sha1_hash(first_part):
			tree_dir = TreeDir(parent=self, name=first_part)
			return tree_dir.create_gitviewfs_object(path_parts[1:])


class TreeDir(GitViewFSObject):
	
	def create_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		first_part = path_parts[0]
		if len(path_parts) == 1:
			tree_dir_item = TreeDirItem(parent=self, name=first_part)
			return tree_dir_item
	
	def list(self):
		items = []
		
		proc = subprocess.Popen(['git', 'cat-file', '-p', self.name], stdout=subprocess.PIPE)
		for line in proc.stdout:
			tab = line.index('\t')
			item = line[tab+1:].strip()
			items.append(item)
		proc.wait()
		
		return items


class TreeDirItem(GitViewFSObject):
	pass


class BlobsDir(GitViewFSObject):
	
	NAME = 'blobs'

	def create_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		first_part = path_parts[0]
		if len(path_parts) == 1  and  self._is_valid_sha1_hash(first_part):
			blob_file = BlobFile(parent=self, name=first_part)
			return blob_file


class BlobFile(GitViewFSObject):
	
	def getattr(self):
		stat_result = super(BlobFile, self).getattr()
		
		attrs = list(stat_result)
		attrs[stat.ST_MODE] = with_regular_file_type(attrs[stat.ST_MODE])
		attrs[stat.ST_MODE] = without_execution_permissions(attrs[stat.ST_MODE])
		attrs[stat.ST_SIZE] = self._get_blob_size()
		return posix.stat_result(attrs)
	
	def _get_blob_size(self):
		subprocess.call(['git', 'cat-file', '-s', self.name])
		size_string = subprocess.check_output(['git', 'cat-file', '-s', self.name])
		size = int(size_string)
		return size
	
	def read(self, length, offset):
		content = subprocess.check_output(['git', 'cat-file', 'blob', self.name])
		return content[offset : offset+length]
