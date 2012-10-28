#!/usr/bin/env python
from __future__ import print_function
import os, sys
import fcntl
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
		return obj.getattr()
	
	def readlink(self, path):
		return os.readlink("." + path)

	def readdir(self, path, offset):
		obj = get_gitviewfs_object(path)
		for item in obj.list():
			yield fuse.Direntry(item)
	
	def unlink(self, path):
		os.unlink("." + path)

	def rmdir(self, path):
		os.rmdir("." + path)

	def symlink(self, path, path1):
		os.symlink(path, "." + path1)

	def rename(self, path, path1):
		os.rename("." + path, "." + path1)

	def link(self, path, path1):
		os.link("." + path, "." + path1)

	def chmod(self, path, mode):
		os.chmod("." + path, mode)

	def chown(self, path, user, group):
		os.chown("." + path, user, group)

	def truncate(self, path, length):
		f = open("." + path, "a")
		f.truncate(length)
		f.close()

	def mknod(self, path, mode, dev):
		os.mknod("." + path, mode, dev)

	def mkdir(self, path, mode):
		os.mkdir("." + path, mode)

	def utime(self, path, times):
		os.utime("." + path, times)

#	The following utimens method would do the same as the above utime method.
#	We can't make it better though as the Python stdlib doesn't know of
#	subsecond preciseness in acces/modify times.
#  
#	def utimens(self, path, ts_acc, ts_mod):
#	  os.utime("." + path, (ts_acc.tv_sec, ts_mod.tv_sec))

	def access(self, path, mode):
		if not os.access("." + path, mode):
			return -errno.EACCES

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
			return self.file.read(length, offset)

		def write(self, buf, offset):
			self.file.seek(offset)
			self.file.write(buf)
			return len(buf)

		def release(self, flags):
			pass

		def _fflush(self):
			pass

		def fsync(self, isfsyncfile):
			self._fflush()
			if isfsyncfile and hasattr(os, 'fdatasync'):
				os.fdatasync(self.fd)
			else:
				os.fsync(self.fd)

		def flush(self):
			pass

		def fgetattr(self):
			return self.file.getattr()

		def ftruncate(self, length):
			self.file.truncate(length)

		def lock(self, cmd, owner, **kw):
			# The code here is much rather just a demonstration of the locking
			# API than something which actually was seen to be useful.

			# Advisory file locking is pretty messy in Unix, and the Python
			# interface to this doesn't make it better.
			# We can't do fcntl(2)/F_GETLK from Python in a platfrom independent
			# way. The following implementation *might* work under Linux. 
			#
			# if cmd == fcntl.F_GETLK:
			#	 import struct
			# 
			#	 lockdata = struct.pack('hhQQi', kw['l_type'], os.SEEK_SET,
			#							kw['l_start'], kw['l_len'], kw['l_pid'])
			#	 ld2 = fcntl.fcntl(self.fd, fcntl.F_GETLK, lockdata)
			#	 flockfields = ('l_type', 'l_whence', 'l_start', 'l_len', 'l_pid')
			#	 uld2 = struct.unpack('hhQQi', ld2)
			#	 res = {}
			#	 for i in xrange(len(uld2)):
			#		  res[flockfields[i]] = uld2[i]
			#  
			#	 return fuse.Flock(**res)

			# Convert fcntl-ish lock parameters to Python's weird
			# lockf(3)/flock(2) medley locking API...
			pass


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
