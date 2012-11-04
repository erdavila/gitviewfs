import unittest

from git_objects_parser import parse_git_commit_content


class TestGitObjectsParser(unittest.TestCase):
	
	AUTHOR_NAME = 'Author Name'
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
				'author ' + self.AUTHOR_NAME + ' <author@domain1.com> 123456789 +0200',
				'committer Name of Committer <committer@domain2.net> 987654321 -0300',
				'',
			) + self.MESSAGE_LINES
		)

	def test_parse_commit_author_name(self):
		commit = parse_git_commit_content(self.commit_content)
		self.assertEqual(self.AUTHOR_NAME, commit.author_name)

	def test_parse_commit_message(self):
		commit = parse_git_commit_content(self.commit_content)
		self.assertEqual(self.join_lines(self.MESSAGE_LINES), commit.message)
	
	def join_lines(self, lines):
		return ''.join(line + '\n' for line in lines)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
