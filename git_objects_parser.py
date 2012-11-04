from collections import namedtuple
import re
import subprocess
import time


Commit = namedtuple('Commit', 'author_name, author_email, author_date, message')

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
	m = re.match(r'author (.+) <(.+)> (.+)', line)
	if m is not None:
		return {
			'author_name'  : m.group(1),
			'author_email' : m.group(2),
			'author_date'  : parse_git_commit_date(m.group(3))
		}
	
	return {}

def parse_git_commit_date(commit_date):
	timestamp, tz = commit_date.split(' ')
	timestamp = int(timestamp)
	timestamp += parse_tz_to_seconds(tz)
	date_string = time.asctime(time.gmtime(timestamp))
	return date_string + ' ' + tz

def parse_tz_to_seconds(tz):
	m = re.match(r'^(\-|\+)(\d\d)(\d\d)$', tz)
	signal = m.group(1)
	hours = int(m.group(2))
	minutes = int(m.group(3))
	
	value_in_seconds = 60*(60*hours + minutes)
	if signal == '-':
		value_in_seconds = -value_in_seconds
	return value_in_seconds
