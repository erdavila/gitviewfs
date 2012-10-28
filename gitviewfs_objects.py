import stat
import posix
import os


OBJECTS_DIR = 'objects'
REMOTES_DIR = 'remotes'


def without_write_permissions(stat_mode):
	stat_mode &= ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
	return stat_mode

def with_symlink_file_type(stat_mode):
	stat_mode = with_clear_file_type(stat_mode)
	stat_mode |= stat.S_IFLNK
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
		
	def list(self):
		return [RefsDir.NAME, OBJECTS_DIR, REMOTES_DIR]


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
