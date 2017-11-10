# Opens the current file for edit in perforce, or open for add if the file isn't already versioned.
# Iterates all p4 clients on the current host to find the one which is the likely parent of the current file.

from scriptlib import *
import os, re, stat, json

class P4Client:
  def __init__(self, clientspec):
    self.name = re.search(r'^Client:\s+(.*)', clientspec, re.MULTILINE).group(1).strip()
    hostmatch = re.search(r'^Host:\s+(.*)', clientspec, re.MULTILINE)
    self.host = hostmatch.group(1).strip() if hostmatch else ''
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
    client_names = sorted([re.sub('Client ', '', match) for match in matches], key=len, reverse=True)

    local_clients = []
    for client_name in client_names:
      client = P4Client(subproc(['p4', 'client', '-o', client_name]))
      if client.host == host:
        local_clients.append(client)

    return local_clients

console.show()

filepath = os.path.abspath(notepad.getCurrentFilename())
console.write('\nFinding parent workspace for ' + filepath)

def get_cached_client_roots_file():
  home = os.path.expanduser("~")
  return os.path.join(home, '.cached_p4_client_roots')

def create_cached_client_roots_file():
  cached_client_roots_file = get_cached_client_roots_file()
  console.write('\nBuilding cache file: ' + cached_client_roots_file)
  f = open(cached_client_roots_file, 'w')
  jsonArr = []
  for client in P4Client.get_local_clients():
    jsonObj = {}
    jsonObj['root'] = client.root
    jsonObj['name'] = client.name
    jsonObj['host'] = client.host
    jsonArr.append(jsonObj)
  f.write(json.dumps(jsonArr, indent=2))
  f.close()

def get_cached_client_roots():
  cached_client_roots_file = get_cached_client_roots_file()
  if not os.path.exists(cached_client_roots_file):
    create_cached_client_roots_file()
  try:
    f = open(cached_client_roots_file)
    return json.loads(f.read())
  finally:
    f.close()

def get_closest_match():
  closest_match = None
  for client in get_cached_client_roots():
    if filepath.upper().find(client['root'].upper()) > -1 and ((not closest_match) or len(client['root']) > len(closest_match['root'])):
      console.write('\nFound match in cache: ' + client['root'])
      closest_match = client
  if not closest_match:
    console.write('\nNo match found in cache.  Force rebuild.')
    os.remove(get_cached_client_roots_file())
    for client in get_cached_client_roots():
      if filepath.upper().find(client['root'].upper()) > -1 and ((not closest_match) or len(client['root']) > len(closest_match['root'])):
        closest_match = client
  return closest_match

closest_match = get_closest_match()
if not closest_match:
  msg = '\nCould not find a parent workspace for ' + filepath
  console.writeError(msg)
else:
  console.write('\nWill checkout from ' + closest_match['name'])
  p4out = subproc(['p4', '-c', closest_match['name'], 'edit', filepath])
  console.write('\n' + p4out)
  if p4out.find('file(s) not on client') > -1:
    console.write('\nThis file is not yet in p4, adding ...')
    p4out = subproc(['p4', '-c', closest_match['name'], 'add', filepath])
    console.write('\n' + p4out)
  else:
    notepad.menuCommand(MENUCOMMAND.EDIT_CLEARREADONLY)
    os.chmod(filepath, stat.S_IWRITE)
    editor.setReadOnly(False)
