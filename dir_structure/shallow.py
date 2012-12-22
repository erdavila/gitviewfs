from dir_structure import DirStructure
from gitviewfs_objects import Directory, HeadSymLink, BranchesProvider,\
	CommitsProvider, TreesProvider, BlobsProvider, CommitMessageFile,\
	CommitPersonNameFile, CommitPersonEmailFile, CommitPersonDateFile,\
	CommitTreeSymLink, CommitParentsProvider, TreeDirItemsProvider, template,\
	DIR_STRUCTURE_CONTEXT_NAME, CommitContextNames, CommitPersonTypes


class Shallow(DirStructure):
	
	def _get_root_dir(self):
		return Directory(name=None, context_values={DIR_STRUCTURE_CONTEXT_NAME:self}, items=[
			HeadSymLink(name='HEAD'),
			self.get_branches_dir(),
			self.get_commits_dir(),
			self.get_trees_dir(),
			self.get_blobs_dir(),
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
		AUTHOR_CONTEXT_VALUES    = {CommitContextNames.PERSON_TYPE:CommitPersonTypes.AUTHOR}
		COMMITTER_CONTEXT_VALUES = {CommitContextNames.PERSON_TYPE:CommitPersonTypes.COMMITTER}
		return template(Directory, items=[
			template(CommitMessageFile, name='message'),
			template(CommitPersonNameFile , name='author-name' , context_values=AUTHOR_CONTEXT_VALUES),
			template(CommitPersonEmailFile, name='author-email', context_values=AUTHOR_CONTEXT_VALUES),
			template(CommitPersonDateFile , name='author-date' , context_values=AUTHOR_CONTEXT_VALUES),
			template(CommitPersonNameFile , name='committer-name' , context_values=COMMITTER_CONTEXT_VALUES),
			template(CommitPersonEmailFile, name='committer-email', context_values=COMMITTER_CONTEXT_VALUES),
			template(CommitPersonDateFile , name='committer-date' , context_values=COMMITTER_CONTEXT_VALUES),
			template(CommitTreeSymLink, name='tree'),
			template(CommitParentsProvider, prefix='parent'),
		])
	
	def _get_tree_dir_template(self):
		return template(Directory, items=[template(TreeDirItemsProvider)])


def get_dir_structure():
	return Shallow()
