# Opens the current file for edit in perforce, or open for add if the file isn't already versioned.
# Iterates all p4 clients on the current host to find the one which is the likely parent of the current file.

from scriptlib import *
import os, re

class P4Client:
  def __init__(self, clientspec):
    self.name = re.search(r'^Client:\s+(.*)', clientspec, re.MULTILINE).group(1).strip()
    self.host = re.search(r'^Host:\s+(.*)', clientspec, re.MULTILINE).group(1).strip()
    self.root = os.path.abspath(re.search(r'^Root:\s+(.*)', clientspec, re.MULTILINE).group(1).strip())

  def __str__(self):
    return self.name + ', ' + self.host + ', ' + self.root

  @staticmethod
  def get_local_clients():
    p4out = subproc(['p4', 'info'])
    user_name = re.search('User name: (.*)', p4out).group(1).strip()
    host = re.search('Client host: (.*)', p4out).group(1).strip()

    p4out = subproc(['p4', 'clients', '-u', user_name])
    matches = re.findall('Client [^ ]+', p4out)
    client_names = [re.sub('Client ', '', match) for match in matches]

    local_clients = []
    for client_name in client_names:
      client = P4Client(subproc(['p4', 'client', '-o', client_name]))
      if client.host == host:
        local_clients.append(client)

    return local_clients

console.show()

filepath = os.path.abspath(notepad.getCurrentFilename())
console.write('\nFinding parent workspace for ' + filepath)

closest_match = None
for client in P4Client.get_local_clients():
  if filepath.find(client.root) > -1 and ((not closest_match) or len(client.root) > len(closest_match.root)):
    closest_match = client

if not closest_match:
  msg = '\nCould not find a parent workspace for ' + filepath
  console.writeError(msg)
else:
  console.write('\nWill checkout from ' + closest_match.name)
  p4out = subproc(['p4', '-c', closest_match.name, 'edit', filepath])
  console.write('\n' + p4out)
  if p4out.find('file(s) not on client') > -1:
    console.write('\nThis file is not yet in p4, adding ...')
    p4out = subproc(['p4', '-c', closest_match.name, 'add', filepath])
    console.write('\n' + p4out)
