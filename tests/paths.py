SAMPLE_HASH = 'a1b2c3d4'
SAMPLE_FILENAME = 'filename'

ROOT_DIR            = '/'
REFS_DIR            = '/refs'
HEAD_SYMLINK        = '/refs/HEAD'
BRANCHES_DIR        = '/refs/branches'
OBJECTS_DIR         = '/objects'
COMMITS_DIR         = '/objects/commits'
COMMIT_DIR	        = '/objects/commits/' + SAMPLE_HASH
COMMIT_TREE_SYMLINK = '/objects/commits/' + SAMPLE_HASH + '/tree'
TREES_DIR           = '/objects/trees'
TREE_DIR 	        = '/objects/trees/' + SAMPLE_HASH
TREE_DIR_ITEM 	    = '/objects/trees/' + SAMPLE_HASH + '/' + SAMPLE_FILENAME
BLOBS_DIR	        = '/objects/blobs'
BLOB_FILE           = '/objects/blobs/' + SAMPLE_HASH

	
class PathMaker(object):
	
	def make_refs_dir_path(self):
		return self.mountpoint + REFS_DIR
	
	def make_head_symlink_path(self):
		return self.mountpoint + HEAD_SYMLINK
	
	def make_branches_dir_path(self):
		return self.mountpoint + BRANCHES_DIR
	
	def make_objects_dir_path(self):
		return self.mountpoint + OBJECTS_DIR
	
	def make_commits_dir_path(self):
		return self.mountpoint + COMMITS_DIR
	
	def make_commit_dir_path(self, commit_sha1):
		return self.mountpoint + COMMIT_DIR.replace(SAMPLE_HASH, commit_sha1)
	
	def make_commit_tree_symlink_path(self, commit_sha1):
		return self.mountpoint + COMMIT_TREE_SYMLINK.replace(SAMPLE_HASH, commit_sha1)
	
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