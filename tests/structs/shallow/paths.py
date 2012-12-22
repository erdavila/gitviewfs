import re

from tests.structs.sample_values import SAMPLE_BRANCH, SAMPLE_HASH,\
	SAMPLE_PARENT, SAMPLE_FILENAME


ROOT_DIR                    = '/'
HEAD_SYMLINK                = '/HEAD'
BRANCHES_DIR                = '/branches'
BRANCH_SYMLINK              = '/branches/' + SAMPLE_BRANCH
COMMITS_DIR                 = '/commits'
COMMIT_DIR                  = '/commits/' + SAMPLE_HASH
COMMIT_MESSAGE_FILE         = '/commits/' + SAMPLE_HASH + '/message'
COMMIT_AUTHOR_NAME_FILE     = '/commits/' + SAMPLE_HASH + '/author-name'
COMMIT_AUTHOR_EMAIL_FILE    = '/commits/' + SAMPLE_HASH + '/author-email'
COMMIT_AUTHOR_DATE_FILE     = '/commits/' + SAMPLE_HASH + '/author-date'
COMMIT_COMMITTER_NAME_FILE  = '/commits/' + SAMPLE_HASH + '/committer-name'
COMMIT_COMMITTER_EMAIL_FILE = '/commits/' + SAMPLE_HASH + '/committer-email'
COMMIT_COMMITTER_DATE_FILE  = '/commits/' + SAMPLE_HASH + '/committer-date'
COMMIT_TREE_SYMLINK         = '/commits/' + SAMPLE_HASH + '/tree'
COMMIT_PARENT_SYMLINK       = '/commits/' + SAMPLE_HASH + '/parent' + SAMPLE_PARENT
TREES_DIR                   = '/trees'
TREE_DIR                    = '/trees/' + SAMPLE_HASH
TREE_DIR_ITEM               = '/trees/' + SAMPLE_HASH + '/' + SAMPLE_FILENAME
BLOBS_DIR                   = '/blobs'
BLOB_FILE                   = '/blobs/' + SAMPLE_HASH


class PathMaker(object):
	
	def make_head_symlink_path(self):
		return self.mountpoint + HEAD_SYMLINK
	
	def make_branches_dir_path(self):
		return self.mountpoint + BRANCHES_DIR
	
	def make_branch_symlink_path(self, branch):
		return self.mountpoint + BRANCH_SYMLINK.replace(SAMPLE_BRANCH, branch)
	
	def make_commits_dir_path(self):
		return self.mountpoint + COMMITS_DIR
	
	def make_commit_dir_path(self, commit_sha1):
		return self.mountpoint + COMMIT_DIR.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_message_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_MESSAGE_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_author_name_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_AUTHOR_NAME_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_author_email_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_AUTHOR_EMAIL_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_committer_name_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_COMMITTER_NAME_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_committer_email_file_path(self, commit_sha1):
		return self.mountpoint + COMMIT_COMMITTER_EMAIL_FILE.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_tree_symlink_path(self, commit_sha1):
		return self.mountpoint + COMMIT_TREE_SYMLINK.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_parent_symlink_path(self, commit_sha1, parent=None):
		path = self.mountpoint + COMMIT_PARENT_SYMLINK.replace(SAMPLE_HASH, commit_sha1)
		if parent is not None:
			path = re.sub(SAMPLE_PARENT + '$', parent, path)
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
