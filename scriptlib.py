import re, subprocess
from Npp import *

def remove_blank_lines(txt):
  new_txt = re.sub('\n[\s\r\n]*\r?\n', '\n', txt)
  return re.sub('^\s*\n', '', new_txt)

def quote_for_sql(txt):
  return "'" + re.sub('\'', '\'\'', txt) + "'"
  
def lines_to_sql_set(txt, xform=lambda txt: txt):
  txt = remove_blank_lines(txt)
  return '(' + ','.join([xform(val) for val in re.split('\r?\n', txt)]) + ')'

def get_current_view_files():
  current_view = notepad.getCurrentView()
  return [file for file in notepad.getFiles() if file[3] == current_view]

# Similar to subprocess.Popen, but automatically return a string containing
# stdout and stderr content, and raise an Exception if the process results in
# a non-zero return code
def subproc(cmd_line):
  # Prevent windows from creating a console window for this command
  startupinfo = subprocess.STARTUPINFO()
  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
  process = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=startupinfo)
  out = process.communicate()[0]
  if process.returncode != 0:
    console.writeError(out)
    raise Exception('p4 command failed: ' + out)
  return out
