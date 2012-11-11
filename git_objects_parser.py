from collections import namedtuple
import re
import subprocess
import time


Commit = namedtuple('Commit', 'parents, author, committer, message')
CommitPerson = namedtuple('CommitPerson', 'name, email, date')


class GitCommitParser(object):
	
	def parse(self, commit_ref_or_sha1):
		commit_content = subprocess.check_output(['git', 'cat-file', 'commit', commit_ref_or_sha1])
		return self.parse_content(commit_content)

	def parse_content(self, commit_content):
		found_message = False
		message = ''
		self._values = { 'parents' : [] }
		for line in commit_content.splitlines(True):
			if found_message:
				message += line
			elif line == '\n':
				found_message = True
			else:
				self.parse_header(line)
		
		return Commit(message=message, **self._values)
	
	def parse_header(self, line):
		m = re.match(r'(author|committer) (.+) <(.+)> (.+)', line)
		if m is not None:
			commit_person_type = m.group(1)
			name = m.group(2)
			email = m.group(3)
			date = self.parse_date(m.group(4))
			commit_person = CommitPerson(name=name, email=email, date=date)
			self._values[commit_person_type] = commit_person
			return
		
		m = re.match(r'parent (.+)', line)
		if m is not None:
			parent_sha1 = m.group(1)
			self._values['parents'].append(parent_sha1)
			return
	
	def parse_date(self, commit_date):
		timestamp, tz = commit_date.split(' ')
		timestamp = int(timestamp)
		timestamp += self.parse_tz_to_seconds(tz)
		date_string = time.asctime(time.gmtime(timestamp))
		return date_string + ' ' + tz

	def parse_tz_to_seconds(self, tz):
		m = re.match(r'^(\-|\+)(\d\d)(\d\d)$', tz)
		signal = m.group(1)
		hours = int(m.group(2))
		minutes = int(m.group(3))
		
		value_in_seconds = 60*(60*hours + minutes)
		if signal == '-':
			value_in_seconds = -value_in_seconds
		return value_in_seconds
