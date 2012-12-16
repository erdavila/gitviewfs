import unittest
import os.path
import re

from git_objects_parser import GitCommitParser, GitTreeParser
from tests.test_with_repository import TestWithRepository


class TestGitCommitParser(unittest.TestCase):
	
	PARENT_1_SHA1 = 'abcdefabcdefabcdefabcdefabcdefabcdefabcd'
	PARENT_2_SHA1 = 'a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2'
	AUTHOR_NAME = 'Author Name'
	AUTHOR_EMAIL = 'author@domain1.com'
	AUTHOR_DATE = '1350852983 -0700'
	AUTHOR_DATE_FORMATTED = 'Sun Oct 21 13:56:23 2012 -0700'
	COMMITTER_NAME = 'Name of Committer'
	COMMITTER_EMAIL = 'committer@domain2.net'
	COMMITTER_DATE = '1350507449 +0100'
	COMMITTER_DATE_FORMATTED = 'Wed Oct 17 21:57:29 2012 +0100'
	MESSAGE_LINES = ( 
		'This is the first line',
		'',
		'... of a commit message',
		'with multiple lines.',
	)
	
	def setUp(self):
		self.commit_content = self.join_lines(
			(
				'tree 0123456789012345678901234567890123456789',
				'parent ' + self.PARENT_1_SHA1,
				'parent ' + self.PARENT_2_SHA1,
				'author '    + self.AUTHOR_NAME    + ' <' + self.AUTHOR_EMAIL    + '> ' + self.AUTHOR_DATE,
				'committer ' + self.COMMITTER_NAME + ' <' + self.COMMITTER_EMAIL + '> ' + self.COMMITTER_DATE,
				'',
			) + self.MESSAGE_LINES
		)
		
		self.parser = GitCommitParser()
	
	def test_parse_commit_parents(self):
		commit = self.parser.parse_content(self.commit_content)
		self.assertSequenceEqual([self.PARENT_1_SHA1, self.PARENT_2_SHA1], commit.parents)
	
	def test_parse_commit_author_name(self):
		commit = self.parser.parse_content(self.commit_content)
		self.assertEqual(self.AUTHOR_NAME, commit.author.name)

	def test_parse_commit_author_email(self):
		commit = self.parser.parse_content(self.commit_content)
		self.assertEqual(self.AUTHOR_EMAIL, commit.author.email)

	def test_parse_commit_author_date(self):
		commit = self.parser.parse_content(self.commit_content)
		self.assertEqual(self.AUTHOR_DATE_FORMATTED, commit.author.date)

	def test_parse_commit_committer_name(self):
		commit = self.parser.parse_content(self.commit_content)
		self.assertEqual(self.COMMITTER_NAME, commit.committer.name)

	def test_parse_commit_committer_email(self):
		commit = self.parser.parse_content(self.commit_content)
		self.assertEqual(self.COMMITTER_EMAIL, commit.committer.email)

	def test_parse_commit_committer_date(self):
		commit = self.parser.parse_content(self.commit_content)
		self.assertEqual(self.COMMITTER_DATE_FORMATTED, commit.committer.date)
	
	def test_commit_date_1(self):
		commit_date = self.AUTHOR_DATE
		parsed_date = self.parser.parse_date(commit_date)
		self.assertEqual(self.AUTHOR_DATE_FORMATTED, parsed_date)
	
	def test_commit_date_2(self):
		commit_date = self.COMMITTER_DATE
		parsed_date = self.parser.parse_date(commit_date)
		self.assertEqual(self.COMMITTER_DATE_FORMATTED, parsed_date)
	
	def test_tz_parsing_1(self):
		seconds = self.parser.parse_tz_to_seconds('-0700')
		self.assertEqual(-7 * 60 * 60, seconds)
	
	def test_tz_parsing_2(self):
		seconds = self.parser.parse_tz_to_seconds('+1234')
		self.assertEqual(12*60*60 + 34*60, seconds)
	
	def test_parse_commit_message(self):
		commit = self.parser.parse_content(self.commit_content)
		self.assertEqual(self.join_lines(self.MESSAGE_LINES), commit.message)
	
	def join_lines(self, lines):
		return ''.join(line + '\n' for line in lines)


class TestGitTreeParser(TestWithRepository):
	
	def test_parse(self):
		FILENAME = 'file.txt'
		SUBDIR = 'subdir'
		if not os.path.isdir(SUBDIR):
			os.makedirs(SUBDIR)
		self.create_and_commit_file(FILENAME)
		self.create_and_commit_file(os.path.join(SUBDIR, 'another-file.txt'))
		
		parser = GitTreeParser()
		tree_items = parser.parse('HEAD^{tree}')
		
		self.assertIn(FILENAME, tree_items)
		self.assertIn(SUBDIR, tree_items)
		
		file_item = tree_items[FILENAME]
		self.assertEqual('100644', file_item.mode)
		self.assertEqual('blob', file_item.type)
		self.assertIsSha1(file_item.sha1)
		self.assertEqual(FILENAME, file_item.name)
		
		dir_item = tree_items[SUBDIR]
		self.assertEqual('040000', dir_item.mode)
		self.assertEqual('tree', dir_item.type)
		self.assertIsSha1(dir_item.sha1)
		self.assertEqual(SUBDIR, dir_item.name)
	
	def assertIsSha1(self, value):
		self.assertTrue(re.match(r'^[0-9a-f]{40}$', value), '%r is not SHA-1' % value)
