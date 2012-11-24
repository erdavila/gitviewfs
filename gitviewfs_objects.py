import stat
import posix
import os
import subprocess
from collections import namedtuple
from abc import abstractmethod, ABCMeta

from git_objects_parser import GitCommitParser


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
		return ROOT_DIR
	
	path_parts = path.split('/')
	assert path_parts[0] == ''
	path_parts.pop(0)
	
	item = ROOT_DIR
	while len(path_parts) > 0 and not isinstance(item, OldGitViewFSObject):
		first_part = path_parts.pop(0)
		item = item.get_item(first_part)
	
	if isinstance(item, OldDirectory):
		return item.get_gitviewfs_object(path_parts)
	
	return item


class OldGitViewFSObject(object):
	
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
	
	def get_stat(self):
		st = self._get_stat()
		return posix.stat_result(st)
	
	def _get_stat(self):
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
	
	def set_parent_dir(self, parent):
		self.parent = parent


def set_parent_dir(item, parent_dir):
	if hasattr(item, 'parent_dir'):
		assert item.parent_dir is parent_dir
	else:
		item.parent_dir = parent_dir


class GitViewFSObject(object):
	
	def __init__(self, name, context_values={}):
		self.name = name
		self.context_values = context_values.copy()
	
	def set_parent_dir(self, parent_dir):
		set_parent_dir(self, parent_dir)
	
	def get_path(self):
		if self.parent_dir.is_root():
			return '/' + self.name
		else:
			return self.parent_dir.get_path() + '/' + self.name
	
	def get_stat(self):
		st = self._get_stat()
		return posix.stat_result(st)
	
	def _get_stat(self):
		st_root = os.lstat('.')
		attrs = list(st_root)
		attrs[stat.ST_MODE] = without_write_permissions(attrs[stat.ST_MODE])
		attrs[stat.ST_NLINK] = 1
		return attrs
	
	def get_context_value(self, name):
		try:
			return self.context_values[name]
		except KeyError:
			return self.parent_dir.get_context_value(name)


class DirItemsProvider(object):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def get_items_names(self): pass
	
	def get_item(self, name):
		item = self._get_item(name)
		item.set_parent_dir(self.parent_dir)
		return item
	
	@abstractmethod
	def _get_item(self, name): pass
	
	def set_parent_dir(self, parent_dir):
		set_parent_dir(self, parent_dir)


class Directory(GitViewFSObject):
	
	def __init__(self, name, items, context_values={}):
		super(Directory, self).__init__(name=name, context_values=context_values)
		self.items = items
		for item in items:
			item.set_parent_dir(self)
	
	def get_items_names(self):
		items_names = []
		for item in self.items:
			if isinstance(item, DirItemsProvider):
				items_names_from_provider = item.get_items_names()
				items_names.extend(items_names_from_provider)
			else:
				items_names.append(item.name)
		return items_names
	
	def get_item(self, name):
		for item in self.items:
			if isinstance(item, DirItemsProvider):
				item_from_provider = item.get_item(name)
				if item_from_provider is not None:
					return item_from_provider
			elif item.name == name:
				return item
	
	def get_path(self):
		if self.is_root():
			return '/'
		else:
			return super(Directory, self).get_path()
	
	def is_root(self):
		return not hasattr(self, 'parent_dir')


class OldDirectory(OldGitViewFSObject):
	
	def _get_stat(self):
		st = super(OldDirectory, self)._get_stat()
		st[stat.ST_MODE] = with_directory_type(st[stat.ST_MODE])
		return st


class PredefinedDirectory(OldDirectory):
	
	def __init__(self, parent, name, items):
		super(PredefinedDirectory, self).__init__(parent=parent, name=name)
		self.items = items
	
	def get_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		first_part = path_parts[0]
		rest = path_parts[1:]
		
		item = self.items[first_part]
		if isinstance(item, OldDirectory):
			return item.get_gitviewfs_object(rest)
		else:
			return item
	
	def get_items_names(self):
		return self.items.keys()


class SymLink(GitViewFSObject):
	__metaclass__ = ABCMeta
	
	def _get_stat(self):
		st = super(SymLink, self)._get_stat()
		st[stat.ST_MODE] = with_symlink_file_type(st[stat.ST_MODE])
		return st
	
	def get_target_path(self):
		target_object = self.get_target_object()
		target_path = target_object.get_path()
		return target_path
	
	@abstractmethod
	def get_target_object(self): pass


class OldSymLink(OldGitViewFSObject):
	
	def _get_stat(self):
		st = super(OldSymLink, self)._get_stat()
		st[stat.ST_MODE] = with_symlink_file_type(st[stat.ST_MODE])
		return st
	
	def get_target_path(self):
		target_object = self.get_target_object()
		target_path = target_object.get_path()
		return target_path


class OldRegularFile(OldGitViewFSObject):
	
	def _get_stat(self):
		st = super(OldRegularFile, self)._get_stat()
		st[stat.ST_MODE] = with_regular_file_type(st[stat.ST_MODE])
		st[stat.ST_MODE] = without_execution_permissions(st[stat.ST_MODE])
		st[stat.ST_SIZE] = self._get_content_size()
		return st
	
	def _get_content_size(self):
		content = self.get_content()
		return len(content)


class RegularFile(GitViewFSObject):
	__metaclass__ = ABCMeta
	
	def _get_stat(self):
		st = super(RegularFile, self)._get_stat()
		st[stat.ST_MODE] = with_regular_file_type(st[stat.ST_MODE])
		st[stat.ST_MODE] = without_execution_permissions(st[stat.ST_MODE])
		st[stat.ST_SIZE] = self._get_content_size()
		return st
	
	def _get_content_size(self):
		content = self.get_content()
		return len(content)
	
	@abstractmethod
	def get_content(self): pass


class template(object):
	
	def __init__(self, Class, **kwargs):
		self.Class = Class
		self.kwargs = kwargs
	
	def create_instance(self, **additional_kwargs):
		kwargs = self.process_kwargs(self.kwargs)
		kwargs.update(self.process_kwargs(additional_kwargs))
		return self.Class(**kwargs)
	
	def process_kwargs(self, kwargs):
		new_kwargs = {}
		for name, value in kwargs.iteritems():
			new_value = self.process_kwarg_value(value)
			new_kwargs[name] = new_value
		return new_kwargs
	
	def process_kwarg_value(self, value):
		if isinstance(value, list):
			return self.process_kwarg_list_value(value)
		else:
			return value
	
	def process_kwarg_list_value(self, list_value):
		new_list_value = []
		for item in list_value:
			if isinstance(item, template):
				new_item = item.create_instance()
			else:
				new_item = item
			new_list_value.append(new_item)

		return new_list_value


class HeadSymLink(SymLink):
	
	def get_target_object(self):
		branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()
		branch_symlink = BRANCHES_DIR.get_item(branch)
		return branch_symlink


class BranchesProvider(DirItemsProvider):
	
	def _get_item(self, name):
		return BranchSymLink(name=name)
	
	def get_items_names(self):
		output = subprocess.check_output(['git', 'rev-parse', '--symbolic', '--branches'])
		branches = output.splitlines()
		return branches


class BranchSymLink(SymLink):
	
	def get_target_object(self):
		branch = self.name
		commit_sha1 = subprocess.check_output(['git', 'rev-parse', branch]).strip()
		commit_dir = COMMITS_DIR.get_item(commit_sha1)
		return commit_dir


class CommitContextNames(object):
	
	SHA1 = 'commit-sha1'
	PERSON_TYPE = 'commit-person-type'
	
	def __init__(self): raise NotImplementedError('should not instantiate this class!')

	
class CommitPersonTypes(object):
	
	AUTHOR = 'author'
	COMMITTER = 'committer'
	
	def __init__(self): raise NotImplementedError('should not instantiate this class!')

	
class CommitsProvider(DirItemsProvider):
	
	def _get_item(self, name):
		context_values = { CommitContextNames.SHA1 : name }
		return COMMIT_DIR_TEMPLATE.create_instance(name=name, context_values=context_values)
	
	def get_items_names(self):
		return []


class CommitMessageFile(RegularFile):
	
	def get_content(self):
		commit_sha1 = self.get_context_value(CommitContextNames.SHA1)
		parser = GitCommitParser()
		commit = parser.parse(commit_sha1)
		return commit.message


class CommitPersonDir(PredefinedDirectory):
	
	PERSON_TYPE_AUTHOR = 'author'
	PERSON_TYPE_COMMITTER = 'committer'
	
	def __init__(self, parent, person_type):
		items = {
			OldCommitPersonNameFile.NAME : OldCommitPersonNameFile(parent=self, person_type=person_type),
			CommitPersonEmailFile.NAME   : CommitPersonEmailFile(parent=self, person_type=person_type),
			CommitPersonDateFile.NAME    : CommitPersonDateFile(parent=self, person_type=person_type),
		}
		super(CommitPersonDir, self).__init__(parent=parent, name=person_type, items=items)
		self.person_type = person_type


class OldCommitPersonDirFile(OldRegularFile):
	
	def __init__(self, parent, person_type):
		super(OldCommitPersonDirFile, self).__init__(parent=parent, name=self.NAME)
		self.person_type = person_type
	
	def _get_commit_person_data(self):
		parsed_commit = self._get_parsed_commit()
		person_type = self.person_type
		person_data = getattr(parsed_commit, person_type)
		return person_data
	
	def _get_parsed_commit(self):
		commit_sha1 = self._get_commit_sha1()
		parser = GitCommitParser()
		parsed_commit = parser.parse(commit_sha1)
		return parsed_commit
	
	def _get_commit_sha1(self):
		commit_person_dir = self.parent
		if isinstance(commit_person_dir, CommitPersonDir):
			commit_dir = commit_person_dir.parent
		else:
			commit_dir = commit_person_dir.parent_dir
		commit_sha1 = commit_dir.name
		return commit_sha1


class CommitPersonItemFile(RegularFile):
	
	def _get_commit_person_data(self):
		parsed_commit = self._get_parsed_commit()
		person_type = self.get_context_value(CommitContextNames.PERSON_TYPE)
		person_data = getattr(parsed_commit, person_type)
		return person_data
	
	def _get_parsed_commit(self):
		commit_sha1 = self.get_context_value(CommitContextNames.SHA1)
		parser = GitCommitParser()
		parsed_commit = parser.parse(commit_sha1)
		return parsed_commit


class CommitPersonNameFile(CommitPersonItemFile):
	
	def get_content(self):
		commit_person_data = self._get_commit_person_data()
		return commit_person_data.name + '\n'


class OldCommitPersonNameFile(OldCommitPersonDirFile):
	
	NAME = 'name'
	
	def get_content(self):
		commit_person_data = self._get_commit_person_data()
		return commit_person_data.name + '\n'


class CommitPersonEmailFile(OldCommitPersonDirFile):
	
	NAME = 'email'
	
	def get_content(self):
		commit_person_data = self._get_commit_person_data()
		return commit_person_data.email + '\n'


class CommitPersonDateFile(OldCommitPersonDirFile):
	
	NAME = 'date'
	
	def get_content(self):
		commit_person_data = self._get_commit_person_data()
		return commit_person_data.date + '\n'


class CommitTreeSymLink(OldSymLink):
	
	NAME = 'tree'
	
	def __init__(self, parent):
		super(CommitTreeSymLink, self).__init__(parent=parent, name=CommitTreeSymLink.NAME)
	
	def get_target_object(self):
		commit_sha1 = self.parent.name
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', commit_sha1 + '^{tree}']).strip()
		trees_dir = TreesDir.INSTANCE
		tree_dir = trees_dir.get_gitviewfs_object([tree_sha1])
		return tree_dir


class CommitParentsDir(OldDirectory):
	
	NAME = 'parents'
	
	def __init__(self, parent):
		super(CommitParentsDir, self).__init__(parent=parent, name=self.NAME)
	
	def get_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		if len(path_parts) == 1:
			parent_num = path_parts[0]
			return CommitParentSymLink(parent=self, name=parent_num)
	
	def get_items_names(self):
		commit_sha1 = self.parent.name
		parser = GitCommitParser()
		commit = parser.parse(commit_sha1)
		num_parents = len(commit.parents)
		num_digits = len(str(num_parents))
		return ['%0*d' % (num_digits, i + 1) for i in range(num_parents)]


class CommitParentSymLink(OldSymLink):
	
	def __init__(self, parent, name):
		assert isinstance(parent, CommitParentsDir)
		super(CommitParentSymLink, self).__init__(parent=parent, name=name)
	
	def get_target_object(self):
		commit_parents_dir = self.parent
		commit_dir = commit_parents_dir.parent
		commit_sha1 = commit_dir.name
		
		parser = GitCommitParser()
		commit = parser.parse(commit_sha1)
		
		parent_number = int(self.name)
		parent_index = parent_number - 1
		parent_sha1 = commit.parents[parent_index]
		
		parent_dir = COMMITS_DIR.get_item(parent_sha1)
		return parent_dir


class TreesDir(OldDirectory):
	
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


class TreeDir(OldDirectory):
	
	def get_gitviewfs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
		
		if len(path_parts) == 1:
			first_part = path_parts[0]
			tree_dir_item = TreeDirItem(parent=self, name=first_part)
			return tree_dir_item
	
	def get_items_names(self):
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


class TreeDirItem(OldSymLink):
	
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


class BlobsDir(OldDirectory):
	
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


class BlobFile(OldRegularFile):
	
	def _get_content_size(self):
		subprocess.call(['git', 'cat-file', '-s', self.name])
		size_string = subprocess.check_output(['git', 'cat-file', '-s', self.name])
		size = int(size_string)
		return size
	
	def get_content(self):
		blob_content = subprocess.check_output(['git', 'cat-file', 'blob', self.name])
		return blob_content


BRANCHES_DIR = Directory(name='branches', items=[BranchesProvider()])
COMMITS_DIR = Directory(name='commits', items=[CommitsProvider()])
ROOT_DIR = Directory(name=None, items=[
	Directory(name='refs', items=[
		HeadSymLink(name='HEAD'),
		BRANCHES_DIR,
	]),
	Directory(name='objects', items=[
		COMMITS_DIR,
		TreesDir(parent=None),
		BlobsDir(parent=None),
	])
])

COMMIT_DIR_TEMPLATE = template(Directory, items=[
	template(CommitMessageFile, name='message'),
	template(Directory, name='author', items=[
		template(OldCommitPersonNameFile , parent=None, person_type=CommitPersonDir.PERSON_TYPE_AUTHOR),
		template(CommitPersonEmailFile, parent=None, person_type=CommitPersonDir.PERSON_TYPE_AUTHOR),
		template(CommitPersonDateFile , parent=None, person_type=CommitPersonDir.PERSON_TYPE_AUTHOR),
	]),
	template(CommitPersonDir  , parent=None, person_type=CommitPersonDir.PERSON_TYPE_COMMITTER),
	template(CommitTreeSymLink, parent=None),
	template(CommitParentsDir , parent=None),
])
