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


def get_gitviewfs_object(path):
	assert path.startswith('/')
	
	if path == '/':
		rest = []
	else:
		path_parts = path.split('/')
		rest = path_parts[1:]
	
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
	
	def __init__(self):
		items = {
			RefsDir.NAME    : RefsDir(parent=self),
			ObjectsDir.NAME : ObjectsDir(parent=self),
			REMOTES_DIR     : None,
		}
		super(RootDir, self).__init__(parent=None, name='/', items=items)
	

class RefsDir(PredefinedDirectory):
	
	NAME = 'refs'
	
	def __init__(self, parent):
		items = {
			HeadSymLink.NAME : HeadSymLink(parent=self),
			'branches'       : None,
			'tags'           : None,
			'remotes'        : None,
		}
		super(RefsDir, self).__init__(parent=parent, name=self.NAME, items=items)


class HeadSymLink(SymLink):
	
	NAME = 'HEAD'
	
	def __init__(self, parent):
		super(HeadSymLink, self).__init__(parent=parent, name=self.NAME)


class ObjectsDir(PredefinedDirectory):
	
	NAME = 'objects'
	
	def __init__(self, parent):
		items = {
			'commits'     : None,
			TreesDir.NAME : TreesDir(parent=self, name=TreesDir.NAME),
			BlobsDir.NAME : BlobsDir(parent=self, name=BlobsDir.NAME),
			'all'         : None,
		}
		super(ObjectsDir, self).__init__(parent=parent, name=self.NAME, items=items)


class TreesDir(Directory):
	
	NAME = 'trees'
	
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
		
		proc = subprocess.Popen(['git', 'cat-file', '-p', self.name], stdout=subprocess.PIPE)
		for line in proc.stdout:
			tab = line.index('\t')
			item = line[tab+1:].strip()
			items.append(item)
		proc.wait()
		
		return items


class TreeDirItem(SymLink):
	pass


class BlobsDir(Directory):
	
	NAME = 'blobs'

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


root_dir = RootDir()
