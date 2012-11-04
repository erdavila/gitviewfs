from collections import namedtuple
import re
import subprocess


Commit = namedtuple('Commit', 'author_name, author_email, message')

def parse_git_commit(commit):
	commit_content = subprocess.check_output(['git', 'cat-file', 'commit', commit])
	return parse_git_commit_content(commit_content)

def parse_git_commit_content(commit_content):
	found_message = False
	message = ''
	values = {}
	for line in commit_content.splitlines(True):
		if found_message:
			message += line
		elif line == '\n':
			found_message = True
		else:
			parsed_header_values = parse_git_commit_header(line)
			values.update(parsed_header_values)
	
	return Commit(message=message, **values)

def parse_git_commit_header(line):
	m = re.match(r'author (.+) <(.+)>', line)
	if m is not None:
		return {
			'author_name' : m.group(1),
			'author_email' : m.group(2),
		}
	
	return {}
