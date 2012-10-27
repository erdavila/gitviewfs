OBJECTS_DIR = 'objects'
REMOTES_DIR = 'remotes'


def create_fs_object(path):
	assert path.startswith('/')
	
	path_parts = path.split('/')
	root_dir = RootDir()
	
	obj = root_dir.create_fs_object(path_parts[1:])
	return obj


class RootDir(object):
	
	PATH = '/'
	
	def create_fs_object(self, path_parts):
		if path_parts == ['']:
			return self
		
		first_part = path_parts[0]
		
		if first_part == RefsDir.NAME:
			refs_dir = RefsDir(parent=self, name=first_part)
			return refs_dir.create_fs_object(path_parts[1:])
	
	def list(self):
		return [RefsDir.NAME, OBJECTS_DIR, REMOTES_DIR]


class RefsDir(object):
	
	NAME = 'refs'
	
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name
	
	def create_fs_object(self, path_parts):
		if len(path_parts) == 0:
			return self
	
	def list(self):
		return ['HEAD', 'branches', 'tags', 'remotes']
