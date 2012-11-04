from collections import namedtuple
import re
import subprocess
import time


Commit = namedtuple('Commit', 'author, committer, message')
CommitPerson = namedtuple('CommitPerson', 'name, email, date')

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
	m = re.match(r'(author|committer) (.+) <(.+)> (.+)', line)
	if m is not None:
		commit_person_type = m.group(1)
		name = m.group(2)
		email = m.group(3)
		date = parse_git_commit_date(m.group(4))
		commit_person = CommitPerson(name=name, email=email, date=date)
		values = { commit_person_type : commit_person, }
		return values
	
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
