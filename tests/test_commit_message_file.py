import unittest

from gitviewfs_objects import get_gitviewfs_object
from tests import paths
import stat
from tests.test_integration import TestIntegration
import subprocess
import os


class TestCommitMessagFile(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_getattr(self):
		commit_message_file = get_gitviewfs_object(paths.COMMIT_MESSAGE_FILE)
		CONTENT_SIZE = 142857
		def _get_content_size():
			return CONTENT_SIZE
		commit_message_file._get_content_size = _get_content_size
		
		attrs = commit_message_file.getattr()
		
		self.assertTrue(stat.S_ISREG(attrs.st_mode))
		
		self.assertFalse(attrs.st_mode & stat.S_IXUSR)
		self.assertFalse(attrs.st_mode & stat.S_IXGRP)
		self.assertFalse(attrs.st_mode & stat.S_IXOTH)
		
		self.assertEqual(CONTENT_SIZE, attrs.st_size)


class TestCommitMessageFileIntegration(TestIntegration):
	
	def setUp(self):
		super(TestCommitMessageFileIntegration, self).setUp()
		self.message = '''
			This is a
			multiline
			commit message
		'''.strip() + '\n'
		self.create_and_commit_file(message=self.message)
		self.commit_sha1 = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
		self.commit_message_path = self.make_commit_message_file_path(self.commit_sha1)
	
	def test_content_size(self):
		st = os.lstat(self.commit_message_path)
		
		self.assertEqual(len(self.message), st.st_size)
	
	def test_content(self):
		with open(self.commit_message_path) as f:
			content = f.read()
		
		self.assertEqual(self.message, content)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_']
	unittest.main()