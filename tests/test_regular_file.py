# -*- encoding: utf-8 -*-
import unittest
from gitviewfs_objects import RegularFile
import stat


class TestRegularFile(unittest.TestCase):
	
	def test_get_stat(self):
		CONTENT_SIZE = 1234
		class MockRegularFile(RegularFile):
			def _get_content_size(self):
				return CONTENT_SIZE
			def get_content(self):
				pass
		reg_file = MockRegularFile(name=None)
		
		st = reg_file._get_stat()
		
		self.assertTrue(stat.S_ISREG(st[stat.ST_MODE]))
		self.assertEqual(stat.S_IXUSR & st[stat.ST_MODE], 0)
		self.assertEqual(stat.S_IXGRP & st[stat.ST_MODE], 0)
		self.assertEqual(stat.S_IXOTH & st[stat.ST_MODE], 0)
		self.assertEqual(st[stat.ST_SIZE], CONTENT_SIZE)
	
	def test_get_content_size_calls_get_content(self):
		CONTENT = '1234567890-=qwertyuiop´[asdfghjklç~]\zxcvbnm,.;/'
		class MockRegularFile(RegularFile):
			def get_content(self):
				return CONTENT
		reg_file = MockRegularFile(name=None)
		
		content_size = reg_file._get_content_size()
		
		self.assertEqual(content_size, len(CONTENT))
