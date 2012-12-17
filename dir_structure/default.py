from dir_structure import DirStructure
from gitviewfs_objects import Directory, HeadSymLink, BranchesProvider,\
	DIR_STRUCTURE_CONTEXT_NAME, COMMITS_DIR, TREES_DIR, BLOBS_DIR


class Default(DirStructure):
	
	def _get_root_dir(self):
		return Directory(name=None, context_values={DIR_STRUCTURE_CONTEXT_NAME:self}, items=[
			Directory(name='refs', items=[
				HeadSymLink(name='HEAD'),
				self.get_branches_dir(),
			]),
			Directory(name='objects', items=[
				COMMITS_DIR,
				TREES_DIR,
				BLOBS_DIR,
			])
		])
	
	def _get_branches_dir(self):
		return Directory(name='branches', items=[BranchesProvider()])
