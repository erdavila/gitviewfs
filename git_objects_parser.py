from collections import namedtuple
import re

Commit = namedtuple('Commit', 'author_name, message')

def parse_git_commit(commit):
	found_message = False
	message = ''
	values = {}
	for line in commit.splitlines(True):
		if found_message:
			message += line
		elif line == '\n':
			found_message = True
		else:
			values.update(parse_git_commit_header(line))
	
	return Commit(message=message, **values)

def parse_git_commit_header(line):
	m = re.match(r'author (.+) <', line)
	if m is not None:
		return { 'author_name' : m.group(1) }
	
	return {}
