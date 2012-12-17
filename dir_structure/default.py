from dir_structure import DirStructure
from gitviewfs_objects import Directory, HeadSymLink, BranchesProvider,\
	CommitsProvider, TREES_DIR, BLOBS_DIR, DIR_STRUCTURE_CONTEXT_NAME


class Default(DirStructure):
	
	def _get_root_dir(self):
		return Directory(name=None, context_values={DIR_STRUCTURE_CONTEXT_NAME:self}, items=[
			Directory(name='refs', items=[
				HeadSymLink(name='HEAD'),
				self.get_branches_dir(),
			]),
			Directory(name='objects', items=[
				self.get_commits_dir(),
				TREES_DIR,
				BLOBS_DIR,
			])
		])
	
	def _get_branches_dir(self):
		return Directory(name='branches', items=[BranchesProvider()])
	
	def _get_commits_dir(self):
		return Directory(name='commits', items=[CommitsProvider()])
