import unittest

from git_objects_parser import GitCommitParser


class TestGitObjectsParser(unittest.TestCase):
	
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
				'parent abcdefabcdefabcdefabcdefabcdefabcdefabcd',
				'parent a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2',
				'author '    + self.AUTHOR_NAME    + ' <' + self.AUTHOR_EMAIL    + '> ' + self.AUTHOR_DATE,
				'committer ' + self.COMMITTER_NAME + ' <' + self.COMMITTER_EMAIL + '> ' + self.COMMITTER_DATE,
				'',
			) + self.MESSAGE_LINES
		)
		
		self.parser = GitCommitParser()

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


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
