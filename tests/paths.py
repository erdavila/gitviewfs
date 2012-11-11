import re
SAMPLE_HASH = 'a1b2c3d4'
SAMPLE_FILENAME = 'filename'
SAMPLE_BRANCH = 'a-branch'
SAMPLE_PARENT = '1'

ROOT_DIR                    = '/'
REFS_DIR                    = '/refs'
HEAD_SYMLINK                = '/refs/HEAD'
BRANCHES_DIR                = '/refs/branches'
BRANCH_SYMLINK              = '/refs/branches/' + SAMPLE_BRANCH
OBJECTS_DIR                 = '/objects'
COMMITS_DIR                 = '/objects/commits'
COMMIT_DIR                  = '/objects/commits/' + SAMPLE_HASH
COMMIT_MESSAGE_FILE         = '/objects/commits/' + SAMPLE_HASH + '/message'
COMMIT_AUTHOR_DIR           = '/objects/commits/' + SAMPLE_HASH + '/author'
COMMIT_AUTHOR_NAME_FILE     = '/objects/commits/' + SAMPLE_HASH + '/author/name'
COMMIT_AUTHOR_EMAIL_FILE    = '/objects/commits/' + SAMPLE_HASH + '/author/email'
COMMIT_AUTHOR_DATE_FILE     = '/objects/commits/' + SAMPLE_HASH + '/author/date'
COMMIT_COMMITTER_DIR        = '/objects/commits/' + SAMPLE_HASH + '/committer'
COMMIT_COMMITTER_NAME_FILE  = '/objects/commits/' + SAMPLE_HASH + '/committer/name'
COMMIT_COMMITTER_EMAIL_FILE = '/objects/commits/' + SAMPLE_HASH + '/committer/email'
COMMIT_COMMITTER_DATE_FILE  = '/objects/commits/' + SAMPLE_HASH + '/committer/date'
COMMIT_TREE_SYMLINK         = '/objects/commits/' + SAMPLE_HASH + '/tree'
COMMIT_PARENTS_DIR          = '/objects/commits/' + SAMPLE_HASH + '/parents'
COMMIT_PARENT_SYMLINK       = '/objects/commits/' + SAMPLE_HASH + '/parents/' + SAMPLE_PARENT
TREES_DIR                   = '/objects/trees'
TREE_DIR                    = '/objects/trees/' + SAMPLE_HASH
TREE_DIR_ITEM               = '/objects/trees/' + SAMPLE_HASH + '/' + SAMPLE_FILENAME
BLOBS_DIR                   = '/objects/blobs'
BLOB_FILE                   = '/objects/blobs/' + SAMPLE_HASH

	
class PathMaker(object):
	
	def make_refs_dir_path(self):
		return self.mountpoint + REFS_DIR
	
	def make_head_symlink_path(self):
		return self.mountpoint + HEAD_SYMLINK
	
	def make_branches_dir_path(self):
		return self.mountpoint + BRANCHES_DIR
	
	def make_branch_symlink_path(self, branch):
		return self.mountpoint + BRANCH_SYMLINK.replace(SAMPLE_BRANCH, branch)
	
	def make_objects_dir_path(self):
		return self.mountpoint + OBJECTS_DIR
	
	def make_commits_dir_path(self):
		return self.mountpoint + COMMITS_DIR
	
	def make_commit_dir_path(self, commit_sha1):
		return self.mountpoint + COMMIT_DIR.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_message_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_MESSAGE_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_author_dir_path(self, commit_sha1):
		return self.mountpoint + COMMIT_AUTHOR_DIR.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_author_name_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_AUTHOR_NAME_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_author_email_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_AUTHOR_EMAIL_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_committer_dir_path(self, commit_sha1):
		return self.mountpoint + COMMIT_COMMITTER_DIR.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_committer_name_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_COMMITTER_NAME_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_committer_email_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_COMMITTER_EMAIL_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_tree_symlink_path(self, commit_sha1):
		return self.mountpoint + COMMIT_TREE_SYMLINK.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_parents_dir_path(self, commit_sha1):
		return self.mountpoint + COMMIT_PARENTS_DIR.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_parent_symlink_path(self, commit_sha1, parent=None):
		path = self.mountpoint + COMMIT_PARENT_SYMLINK.replace(SAMPLE_HASH, commit_sha1)
		if parent is not None:
			path = re.sub(r'/' + SAMPLE_PARENT + '$', '/' + parent, path)
		return path
	
	def make_trees_dir_path(self):
		return self.mountpoint + TREES_DIR
	
	def make_tree_dir_path(self, tree_sha1):
		return self.mountpoint + TREE_DIR.replace(SAMPLE_HASH, tree_sha1)
	
	def make_tree_dir_item_path(self, tree_sha1, item_name):
		return self.mountpoint + TREE_DIR_ITEM.replace(SAMPLE_HASH, tree_sha1).replace(SAMPLE_FILENAME, item_name)
	
	def make_blobs_dir_path(self):
		return self.mountpoint + BLOBS_DIR
	
	def make_blob_file_path(self, blob_sha1):
		return self.mountpoint + BLOB_FILE.replace(SAMPLE_HASH, blob_sha1)
