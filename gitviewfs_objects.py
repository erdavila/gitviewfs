import stat
import posix
import os
import subprocess
from collections import namedtuple
from git_objects_parser import parse_git_commit


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

def with_directory_type(stat_mode):
	stat_mode = with_clear_file_type(stat_mode)
	stat_mode |= stat.S_IFDIR
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
		attrs = self._get_attrs()
		return posix.stat_result(attrs)
	
	def _get_attrs(self):
		st_root = os.lstat('.')
		attrs = list(st_root)
		attrs[stat.ST_MODE] = without_write_permissions(attrs[stat.ST_MODE])
		attrs[stat.ST_NLINK] = 1
		return attrs
	
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
	
	def _get_attrs(self):
		attrs = super(Directory, self)._get_attrs()
		attrs[stat.ST_MODE] = with_directory_type(attrs[stat.ST_MODE])
		return attrs


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
	
	def _get_attrs(self):
		attrs = super(SymLink, self)._get_attrs()
		attrs[stat.ST_MODE] = with_symlink_file_type(attrs[stat.ST_MODE])
		return attrs
	
	def readlink(self):
		target_object = self.get_target_object()
		
		target_path = target_object.get_path()
		symlink_path = os.path.relpath(target_path, self.parent.get_path())
		return symlink_path


class RegularFile(GitViewFSObject):
	
	def read(self, length, offset):
		content = self._get_content()
		return content[offset : offset+length]
	
	def _get_attrs(self):
		attrs = super(RegularFile, self)._get_attrs()
		attrs[stat.ST_MODE] = with_regular_file_type(attrs[stat.ST_MODE])
		attrs[stat.ST_MODE] = without_execution_permissions(attrs[stat.ST_MODE])
		attrs[stat.ST_SIZE] = self._get_content_size()
		return attrs
	
	def _get_content_size(self):
		content = self._get_content()
		return len(content)


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
			BranchesDir.NAME : BranchesDir(parent=self),
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
	
	def get_target_object(self):
		branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()
		branches_dir = BranchesDir.INSTANCE
		branch_symlink = branches_dir.get_gitviewfs_object([branch])
		return branch_symlink


class BranchesDir(Directory):
	
	NAME = 'branches'
	INSTANCE = None
	
	def __init__(self, parent):
		super(BranchesDir, self).__init__(parent=parent, name=self.NAME)
		BranchesDir.INSTANCE = self
	
	def get_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		if len(path_parts) == 1:
			first_part = path_parts[0]
			tree_dir_item = BranchSymLink(parent=self, name=first_part)
			return tree_dir_item
	
	def list(self):
		output = subprocess.check_output(['git', 'rev-parse', '--symbolic', '--branches'])
		branches = output.splitlines()
		return branches


class BranchSymLink(SymLink):
	
	def get_target_object(self):
		branch = self.name
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', branch]).strip()
		commits_dir = CommitsDir.INSTANCE
		commit_dir = commits_dir.get_gitviewfs_object([commit_sha1])
		return commit_dir


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
			CommitMessageFile.NAME  : CommitMessageFile(parent=self),
			CommitAuthorDir.NAME    : CommitAuthorDir(parent=self),
			CommitCommitterDir.NAME : CommitCommitterDir(parent=self),
			'parents'               : None,
			CommitTreeSymLink.NAME  : CommitTreeSymLink(parent=self),
		}
		super(CommitDir, self).__init__(parent=parent, name=name, items=items)


class CommitMessageFile(RegularFile):
	
	NAME = 'message'
	
	def __init__(self, parent):
		super(CommitMessageFile, self).__init__(parent=parent, name=self.NAME)
	
	def _get_content(self):
		commit_sha1 = self.parent.name
		commit = parse_git_commit(commit_sha1)
		return commit.message


class CommitPersonDir(PredefinedDirectory):
	
	def __init__(self, parent):
		assert isinstance(parent, CommitDir)
		items = {
			CommitPersonNameFile.NAME  : CommitPersonNameFile(parent=self),
			CommitPersonEmailFile.NAME : CommitPersonEmailFile(parent=self),
			CommitAuthorDateFile.NAME  : CommitAuthorDateFile(parent=self),
		}
		super(CommitPersonDir, self).__init__(parent=parent, name=self.NAME, items=items)


class CommitAuthorDir(CommitPersonDir):
	
	NAME = 'author'


class CommitCommitterDir(CommitPersonDir):
	
	NAME = 'committer'


class CommitPersonDirFile(RegularFile):
	
	def __init__(self, parent):
		assert isinstance(parent, CommitPersonDir)
		super(CommitPersonDirFile, self).__init__(parent=parent, name=self.NAME)
	
	def _get_commit_person_data(self):
		parsed_commit = self._get_parsed_commit()
		person_type = self.parent.name
		person_data = getattr(parsed_commit, person_type)
		return person_data
	
	def _get_parsed_commit(self):
		commit_sha1 = self._get_commit_sha1()
		parsed_commit = parse_git_commit(commit_sha1)
		return parsed_commit
	
	def _get_commit_sha1(self):
		commit_person_dir = self.parent
		commit_dir = commit_person_dir.parent
		commit_sha1 = commit_dir.name
		return commit_sha1


class CommitPersonNameFile(CommitPersonDirFile):
	
	NAME = 'name'
	
	def _get_content(self):
		commit_person_data = self._get_commit_person_data()
		return commit_person_data.name + '\n'


class CommitPersonEmailFile(CommitPersonDirFile):
	
	NAME = 'email'
	
	def _get_content(self):
		commit_person_data = self._get_commit_person_data()
		return commit_person_data.email + '\n'


class CommitAuthorDateFile(CommitPersonDirFile):
	
	NAME = 'date'
	
	def _get_content(self):
		parsed_commit = self._get_parsed_commit()
		return parsed_commit.author.date + '\n'


class CommitTreeSymLink(SymLink):
	
	NAME = 'tree'
	
	def __init__(self, parent):
		assert isinstance(parent, CommitDir)
		super(CommitTreeSymLink, self).__init__(parent=parent, name=CommitTreeSymLink.NAME)
	
	def get_target_object(self):
		commit_sha1 = self.parent.name
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', commit_sha1 + '^{tree}']).strip()
		trees_dir = TreesDir.INSTANCE
		tree_dir = trees_dir.get_gitviewfs_object([tree_sha1])
		return tree_dir


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
		
		if len(path_parts) == 1:
			first_part = path_parts[0]
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
	
	def get_target_object(self):
		for item in self.parent._read_tree_items():
			if item.name == self.name:
				break
		
		if item.type == 'blob':
			dir_object = BlobsDir.INSTANCE
		elif item.type == 'tree':
			dir_object = TreesDir.INSTANCE
		
		target_object = dir_object.get_gitviewfs_object([item.sha1])
		return target_object


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


class BlobFile(RegularFile):
	
	def _get_content_size(self):
		subprocess.call(['git', 'cat-file', '-s', self.name])
		size_string = subprocess.check_output(['git', 'cat-file', '-s', self.name])
		size = int(size_string)
		return size
	
	def _get_content(self):
		blob_content = subprocess.check_output(['git', 'cat-file', 'blob', self.name])
		return blob_content


RootDir()
