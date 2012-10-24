REFS_DIR = 'refs'
OBJECTS_DIR = 'objects'
REMOTES_DIR = 'remotes'


class RootDir(object):
	
	PATH = '/'
	
	def list(self):
		return [REFS_DIR, OBJECTS_DIR, REMOTES_DIR]
