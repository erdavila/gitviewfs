from dir_structure import DirStructure
from gitviewfs_objects import Directory, HeadSymLink, BRANCHES_DIR, COMMITS_DIR,\
	TREES_DIR, BLOBS_DIR


class Default(DirStructure):
	
	def _get_root_dir(self):
		return Directory(name=None, items=[
			Directory(name='refs', items=[
				HeadSymLink(name='HEAD'),
				BRANCHES_DIR,
			]),
			Directory(name='objects', items=[
				COMMITS_DIR,
				TREES_DIR,
				BLOBS_DIR,
			])
		])
