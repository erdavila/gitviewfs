import stat
import posix
import os
import subprocess
from abc import abstractmethod, ABCMeta

from git_objects_parser import GitCommitParser, GitTreeParser


DIR_STRUCTURE_CONTEXT_NAME = 'dir-structure'


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


def set_parent_dir(item, parent_dir):
	if hasattr(item, 'parent_dir'):
		assert item.parent_dir is parent_dir, '%r is not %r' % (item.parent_dir, parent_dir)
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
		if item is not None:
			item.set_parent_dir(self.parent_dir)
			return item
	
	@abstractmethod
	def _get_item(self, name): pass
	
	def set_parent_dir(self, parent_dir):
		set_parent_dir(self, parent_dir)
	
	def get_context_value(self, name):
		return self.parent_dir.get_context_value(name)


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
		dir_struct = self.get_context_value(DIR_STRUCTURE_CONTEXT_NAME)
		branches_dir = dir_struct.get_branches_dir()
		branch_symlink = branches_dir.get_item(branch)
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
		dir_struct = self.get_context_value(DIR_STRUCTURE_CONTEXT_NAME)
		commits_dir = dir_struct.get_commits_dir()
		commit_dir = commits_dir.get_item(commit_sha1)
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
		dir_struct = self.parent_dir.get_context_value(DIR_STRUCTURE_CONTEXT_NAME)
		commit_dir_template = dir_struct.get_commit_dir_template()
		
		context_values = { CommitContextNames.SHA1 : name }
		return commit_dir_template.create_instance(name=name, context_values=context_values)
	
	def get_items_names(self):
		return []


class CommitMessageFile(RegularFile):
	
	def get_content(self):
		commit_sha1 = self.get_context_value(CommitContextNames.SHA1)
		parser = GitCommitParser()
		commit = parser.parse(commit_sha1)
		return commit.message


class CommitPersonItemFile(RegularFile):
	
	def _get_commit_person_data(self):
		parsed_commit = self._get_parsed_commit()
		person_type = self.get_context_value(CommitContextNames.PERSON_TYPE)
		parsed_commit_attribute = person_type
		person_data = getattr(parsed_commit, parsed_commit_attribute)
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


class CommitPersonEmailFile(CommitPersonItemFile):
	
	def get_content(self):
		commit_person_data = self._get_commit_person_data()
		return commit_person_data.email + '\n'


class CommitPersonDateFile(CommitPersonItemFile):
	
	def get_content(self):
		commit_person_data = self._get_commit_person_data()
		return commit_person_data.date + '\n'
	

class CommitTreeSymLink(SymLink):
	
	def get_target_object(self):
		commit_sha1 = self.get_context_value(CommitContextNames.SHA1)
		tree_sha1 = subprocess.check_output(['git', 'rev-parse', commit_sha1 + '^{tree}']).strip()
		
		dir_struct = self.get_context_value(DIR_STRUCTURE_CONTEXT_NAME)
		trees_dir = dir_struct.get_trees_dir()
		tree_dir = trees_dir.get_item(tree_sha1)
		
		return tree_dir


class CommitParentsProvider(DirItemsProvider):
	
	def __init__(self, prefix=''):
		self.prefix = prefix
	
	def _get_item(self, name):
		if name.startswith(self.prefix):
			parent_number_string = name[len(self.prefix):]
			try:
				parent_number = int(parent_number_string, 10)
			except ValueError:
				pass
			else:
				return CommitParentSymLink(name=name, parent_number=parent_number)
	
	def get_items_names(self):
		parser = GitCommitParser()
		commit_sha1 = self.get_context_value(CommitContextNames.SHA1)
		commit = parser.parse(commit_sha1)
		num_parents = len(commit.parents)
		num_digits = len(str(num_parents))
		return ['%s%0*d' % (self.prefix, num_digits, i + 1) for i in xrange(num_parents)]


class CommitParentSymLink(SymLink):
	
	def __init__(self, name, parent_number):
		super(CommitParentSymLink, self).__init__(name=name)
		self.parent_number = parent_number
	
	def get_target_object(self):
		commit_sha1 = self.get_context_value(CommitContextNames.SHA1)
		
		parser = GitCommitParser()
		commit = parser.parse(commit_sha1)
		
		parent_index = self.parent_number - 1
		parent_sha1 = commit.parents[parent_index]
		
		dir_struct = self.get_context_value(DIR_STRUCTURE_CONTEXT_NAME)
		commits_dir = dir_struct.get_commits_dir()
		parent_commit_dir = commits_dir.get_item(parent_sha1)
		
		return parent_commit_dir


class TreesProvider(DirItemsProvider):
	
	def get_items_names(self):
		return []
	
	def _get_item(self, name):
		dir_struct = self.parent_dir.get_context_value(DIR_STRUCTURE_CONTEXT_NAME)
		tree_dir_template = dir_struct.get_tree_dir_template()
		
		context_values = {TreeContextNames.SHA1:name}
		return tree_dir_template.create_instance(name=name, context_values=context_values)


class TreeContextNames(object):
	
	SHA1 = 'tree-sha1'
	
	def __init__(self): raise NotImplementedError('should not instantiate this class!')


class TreeDirItemsProvider(DirItemsProvider):
	
	def get_items_names(self):
		tree_sha1 = self.parent_dir.get_context_value(TreeContextNames.SHA1)
		parser = GitTreeParser()
		items = parser.parse(tree_sha1)
		return items.keys()
	
	def _get_item(self, name):
		return TreeDirItem(name=name)


class TreeDirItem(SymLink):
	
	def get_target_object(self):
		tree_sha1 = self.get_context_value(TreeContextNames.SHA1)
		parser = GitTreeParser()
		items = parser.parse(tree_sha1)
		item = items[self.name]
		
		dir_struct = self.get_context_value(DIR_STRUCTURE_CONTEXT_NAME)
		
		if item.type == 'blob':
			target_dir = dir_struct.get_blobs_dir()
		elif item.type == 'tree':
			target_dir = dir_struct.get_trees_dir()
		
		target_object = target_dir.get_item(item.sha1)
		
		return target_object


class BlobsProvider(DirItemsProvider):
	
	def get_items_names(self):
		return []
	
	def _get_item(self, name):
		return BlobFile(name=name)


class BlobFile(RegularFile):
	
	def get_content(self):
		blob_sha1 = self.name
		blob_content = subprocess.check_output(['git', 'cat-file', 'blob', blob_sha1])
		return blob_content
	
	def _get_content_size(self):
		size_string = subprocess.check_output(['git', 'cat-file', '-s', self.name])
		size = int(size_string)
		return size
