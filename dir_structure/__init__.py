from abc import abstractmethod, ABCMeta

from gitviewfs_objects import ROOT_DIR


class DirStructure(object):
	__metaclass__ = ABCMeta
	
	def get_object(self, path):
		assert path.startswith('/')
		
		if path == '/':
			return ROOT_DIR
		
		path_parts = path.split('/')
		assert path_parts[0] == ''
		path_parts.pop(0)
		
		item = ROOT_DIR
		while len(path_parts) > 0:
			first_part = path_parts.pop(0)
			item = item.get_item(first_part)
		
		return item
