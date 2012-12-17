from abc import abstractmethod, ABCMeta


class DirStructure(object):
	__metaclass__ = ABCMeta
	
	def get_object(self, path):
		assert path.startswith('/')
		
		if path == '/':
			return self.get_root_dir()
		
		path_parts = path.split('/')
		assert path_parts[0] == ''
		path_parts.pop(0)
		
		item = self.get_root_dir()
		while len(path_parts) > 0:
			first_part = path_parts.pop(0)
			item = item.get_item(first_part)
		
		return item
	
	def  get_root_dir(self): return self.__get_cached_attribute('root_dir')
	@abstractmethod
	def _get_root_dir(self): pass
	
	def  get_branches_dir(self): return self.__get_cached_attribute('branches_dir')
	@abstractmethod
	def _get_branches_dir(self): pass
	
	def  get_commits_dir(self): return self.__get_cached_attribute('commits_dir')
	@abstractmethod
	def _get_commits_dir(self): pass
	
	def  get_trees_dir(self): return self.__get_cached_attribute('trees_dir')
	@abstractmethod
	def _get_trees_dir(self): pass
	
	def __get_cached_attribute(self, attribute):
		try:
			value = getattr(self, attribute)
		except AttributeError:
			getter_method_name = '_get_' + attribute
			getter_method = getattr(self, getter_method_name)
			value = getter_method()
			setattr(self, attribute, value)
		return value
