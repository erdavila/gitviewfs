from dir_structure import DirStructure
from gitviewfs_objects import Directory, HeadSymLink, BranchesProvider,\
	CommitsProvider, TreesProvider, BlobsProvider, CommitMessageFile,\
	CommitPersonNameFile, CommitPersonEmailFile, CommitPersonDateFile,\
	CommitTreeSymLink, CommitParentsProvider, TreeDirItemsProvider, template,\
	DIR_STRUCTURE_CONTEXT_NAME, CommitContextNames, CommitPersonTypes


class Default(DirStructure):
	
	def _get_root_dir(self):
		return Directory(name=None, context_values={DIR_STRUCTURE_CONTEXT_NAME:self}, items=[
			Directory(name='refs', items=[
				HeadSymLink(name='HEAD'),
				self.get_branches_dir(),
			]),
			Directory(name='objects', items=[
				self.get_commits_dir(),
				self.get_trees_dir(),
				self.get_blobs_dir(),
			])
		])
	
	def _get_branches_dir(self):
		return Directory(name='branches', items=[BranchesProvider()])
	
	def _get_commits_dir(self):
		return Directory(name='commits', items=[CommitsProvider()])
	
	def _get_trees_dir(self):
		return Directory(name='trees', items=[TreesProvider()])
	
	def _get_blobs_dir(self):
		return Directory(name='blobs', items=[BlobsProvider()])
	
	def _get_commit_dir_template(self):
		return template(Directory, items=[
			template(CommitMessageFile, name='message'),
			template(Directory, name='author', context_values={CommitContextNames.PERSON_TYPE:CommitPersonTypes.AUTHOR}, items=[
				template(CommitPersonNameFile , name='name' ),
				template(CommitPersonEmailFile, name='email'),
				template(CommitPersonDateFile , name='date' ),
			]),
			template(Directory, name='committer', context_values={CommitContextNames.PERSON_TYPE:CommitPersonTypes.COMMITTER}, items=[
				template(CommitPersonNameFile , name='name' ),
				template(CommitPersonEmailFile, name='email'),
				template(CommitPersonDateFile , name='date' ),
			]),
			template(CommitTreeSymLink, name='tree'),
			template(Directory, name='parents', items=[template(CommitParentsProvider)])
		])
	
	def _get_tree_dir_template(self):
		return template(Directory, items=[template(TreeDirItemsProvider)])
