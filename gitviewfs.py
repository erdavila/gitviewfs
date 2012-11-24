#!/usr/bin/env python
from __future__ import print_function
import os, sys
import fuse
from fuse import Fuse
from gitviewfs_objects import get_gitviewfs_object
import errno


if not hasattr(fuse, '__version__'):
	raise RuntimeError, \
		"your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

fuse.feature_assert('stateful_files', 'has_init')


class GitViewFS(Fuse):

	def __init__(self, *args, **kw):
		Fuse.__init__(self, *args, **kw)

		# do stuff to set up your filesystem here, if you want
		#import thread
		#thread.start_new_thread(self.mythread, ())
		self.repo = '.'

#	def mythread(self):
#
#		"""
#		The beauty of the FUSE python implementation is that with the python interp
#		running in foreground, you can have threads
#		"""
#		print "mythread: started"
#		while 1:
#			time.sleep(120)
#			print "mythread: ticking"

	def getattr(self, path):
		obj = get_gitviewfs_object(path)
		return obj.get_stat()
	
	def readlink(self, path):
		symlink = get_gitviewfs_object(path)
		target_path = symlink.get_target_path()
		parent_path, _ = os.path.split(path)
		relative_target_path = os.path.relpath(target_path, parent_path)
		return relative_target_path

	def readdir(self, path, offset):
		obj = get_gitviewfs_object(path)
		for item_name in obj.get_items_names():
			yield fuse.Direntry(item_name)

	'''
	def access(self, path, mode):
		if not os.access("." + path, mode):
			return -errno.EACCES
	'''

#	This is how we could add stub extended attribute handlers...
#	(We can't have ones which aptly delegate requests to the underlying fs
#	because Python lacks a standard xattr interface.)
#
#	def getxattr(self, path, name, size):
#		val = name.swapcase() + '@' + path
#		if size == 0:
#			# We are asked for size of the value.
#			return len(val)
#		return val
#
#	def listxattr(self, path, size):
#		# We use the "user" namespace to please XFS utils
#		aa = ["user." + a for a in ("foo", "bar")]
#		if size == 0:
#			# We are asked for size of the attr list, ie. joint size of attrs
#			# plus null separators.
#			return len("".join(aa)) + len(aa)
#		return aa

	def statfs(self):
		"""
		Should return an object with statvfs attributes (f_bsize, f_frsize...).
		Eg., the return value of os.statvfs() is such a thing (since py 2.2).
		If you are not reusing an existing statvfs object, start with
		fuse.StatVFS(), and define the attributes.

		To provide usable information (ie., you want sensible df(1)
		output, you are suggested to specify the following attributes:

			- f_bsize - preferred size of file blocks, in bytes
			- f_frsize - fundamental size of file blcoks, in bytes
				[if you have no idea, use the same as blocksize]
			- f_blocks - total number of blocks in the filesystem
			- f_bfree - number of free blocks
			- f_files - total number of file inodes
			- f_ffree - nunber of free file inodes
		"""
		return os.statvfs(".")

	def fsinit(self):
		os.chdir(self.repo)

	class GitViewFSFile(object):

		def __init__(self, path, flags, *mode):
			self.file = get_gitviewfs_object(path)

		def read(self, length, offset):
			content = self.file.get_content()
			return content[offset : offset+length]

		def fgetattr(self):
			return self.file.get_stat()

	def main(self, *a, **kw):
		self.file_class = self.GitViewFSFile
		return Fuse.main(self, *a, **kw)


def main():

	server = GitViewFS(version="%prog 0.1", dash_s_do='setsingle')

	# Disable multithreading: if you want to use it, protect all method of
	# XmlFile class with locks, in order to prevent race conditions
	server.multithreaded = False

	server.parser.add_option(mountopt="repo", metavar="PATH", default='.',
							 help="browse Git repository from under PATH [default: %default]")
	server.parse(values=server, errex=1)

	try:
		if server.fuse_args.mount_expected():
			os.chdir(server.repo)
	except OSError:
		print("can't enter Git repo directory", file=sys.stderr)
		sys.exit(1)

	server.main()


if __name__ == '__main__':
	main()
