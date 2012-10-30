import stat
import posix
import os
import subprocess
from collections import namedtuple


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


def get_gitviewfs_object(path):
	assert path.startswith('/')
	
	if path == '/':
		rest = []
	else:
		path_parts = path.split('/')
		rest = path_parts[1:]
	
	root_dir = RootDir.INSTANCE
	obj = root_dir.get_gitviewfs_object(rest)
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
	
	def get_path(self):
		parent_path = self.parent.get_path()
		if parent_path == '/':
			path = '/' + self.name
		else:
			path = parent_path + '/' + self.name
		return path
	
	def _is_valid_sha1_hash(self, sha1_hash):
		return 4 <= len(sha1_hash) <= 40


class Directory(GitViewFSObject):
	pass


class PredefinedDirectory(Directory):
	
	def __init__(self, parent, name, items):
		super(PredefinedDirectory, self).__init__(parent=parent, name=name)
		self.items = items
	
	def get_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		first_part = path_parts[0]
		rest = path_parts[1:]
		
		item = self.items[first_part]
		if isinstance(item, Directory):
			return item.get_gitviewfs_object(rest)
		else:
			return item
	
	def list(self):
		return self.items.keys()


class SymLink(GitViewFSObject):
	
	def getattr(self):
		stat_result = super(SymLink, self).getattr()
		
		attrs = list(stat_result)
		attrs[stat.ST_MODE] = with_symlink_file_type(attrs[stat.ST_MODE])
		return posix.stat_result(attrs)


class RootDir(PredefinedDirectory):
	
	INSTANCE = None
	
	def __init__(self):
		items = {
			RefsDir.NAME    : RefsDir(parent=self),
			ObjectsDir.NAME : ObjectsDir(parent=self),
			REMOTES_DIR     : None,
		}
		super(RootDir, self).__init__(parent=None, name='/', items=items)
		RootDir.INSTANCE = self
	
	def get_path(self):
		return '/'
	

class RefsDir(PredefinedDirectory):
	
	NAME = 'refs'
	INSTANCE = None
	
	def __init__(self, parent):
		items = {
			HeadSymLink.NAME : HeadSymLink(parent=self),
			'branches'       : None,
			'tags'           : None,
			'remotes'        : None,
		}
		super(RefsDir, self).__init__(parent=parent, name=self.NAME, items=items)
		RefsDir.INSTANCE = self


class HeadSymLink(SymLink):
	
	NAME = 'HEAD'
	INSTANCE = None
	
	def __init__(self, parent):
		super(HeadSymLink, self).__init__(parent=parent, name=self.NAME)
		HeadSymLink.INSTANCE = self


class ObjectsDir(PredefinedDirectory):
	
	NAME = 'objects'
	INSTANCE = None
	
	def __init__(self, parent):
		items = {
			CommitsDir.NAME : CommitsDir(parent=self),
			TreesDir.NAME   : TreesDir(parent=self),
			BlobsDir.NAME   : BlobsDir(parent=self),
			'all'           : None,
		}
		super(ObjectsDir, self).__init__(parent=parent, name=self.NAME, items=items)
		ObjectsDir.INSTANCE = self


class CommitsDir(Directory):
	
	NAME = 'commits'
	INSTANCE = None
	
	def __init__(self, parent):
		super(CommitsDir, self).__init__(parent=parent, name=self.NAME)
		CommitsDir.INSTANCE = self
	
	def get_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		first_part = path_parts[0]
		rest = path_parts[1:]
		if self._is_valid_sha1_hash(first_part):
			commit_dir = CommitDir(parent=self, name=first_part)
			return commit_dir.get_gitviewfs_object(rest)


class CommitDir(PredefinedDirectory):
	
	def __init__(self, parent, name):
		items = {
			'message'              : None,
			'author'               : None,
			'committer'            : None,
			'parents'              : None,
			CommitTreeSymLink.NAME : CommitTreeSymLink(parent=self),
		}
		super(CommitDir, self).__init__(parent=parent, name=name, items=items)


class CommitTreeSymLink(SymLink):
	
	NAME = 'tree'
	
	def __init__(self, parent):
		assert isinstance(parent, CommitDir)
		super(CommitTreeSymLink, self).__init__(parent=parent, name=CommitTreeSymLink.NAME)


class TreesDir(Directory):
	
	NAME = 'trees'
	INSTANCE = None
	
	def __init__(self, parent):
		super(TreesDir, self).__init__(parent=parent, name=self.NAME)
		TreesDir.INSTANCE = self
	
	def get_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		first_part = path_parts[0]
		if self._is_valid_sha1_hash(first_part):
			tree_dir = TreeDir(parent=self, name=first_part)
			return tree_dir.get_gitviewfs_object(path_parts[1:])


class TreeDir(Directory):
	
	def get_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		first_part = path_parts[0]
		if len(path_parts) == 1:
			tree_dir_item = TreeDirItem(parent=self, name=first_part)
			return tree_dir_item
	
	def list(self):
		items = []
		
		for item in self._read_tree_items():
			items.append(item.name)
		
		return items
	
	Item = namedtuple('Item', 'name, sha1, type, perms')
	
	def _read_tree_items(self):
		tree_sha1 = self.name
		proc = subprocess.Popen(['git', 'cat-file', '-p', tree_sha1], stdout=subprocess.PIPE)
		try:
			for line in proc.stdout:
				line = line.strip()
				perms_and_type_and_sha1, item_name = line.split('\t')
				item_perms, item_type, item_sha1 = perms_and_type_and_sha1.split(' ')
				yield self.Item(item_name, item_sha1, item_type, item_perms)
		finally:
			proc.wait()


class TreeDirItem(SymLink):
	
	def __init__(self, parent, name):
		assert isinstance(parent, TreeDir)
		super(TreeDirItem, self).__init__(parent, name)
	
	
	def readlink(self):
		for item in self.parent._read_tree_items():
			if item.name == self.name:
				break
		
		if item.type == 'blob':
			dir_object = BlobsDir.INSTANCE
		elif item.type == 'tree':
			dir_object = TreesDir.INSTANCE
		
		target_object = dir_object.get_gitviewfs_object([item.sha1])
		target_path = target_object.get_path()
		symlink_path = os.path.relpath(target_path, self.parent.get_path())
		return symlink_path


class BlobsDir(Directory):
	
	NAME = 'blobs'
	INSTANCE = None
	
	def __init__(self, parent):
		super(BlobsDir, self).__init__(parent=parent, name=self.NAME)
		BlobsDir.INSTANCE = self
	
	def get_gitviewfs_object(self, path_parts):
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


RootDir()
