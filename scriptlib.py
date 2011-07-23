import re
from Npp import *

def remove_blank_lines(txt):
  return re.compile('(^\r?\n)|(\r?\n$)', re.MULTILINE).sub('', txt)

def quote_for_sql(txt):
  return "'" + re.sub('\'', '\'\'', txt) + "'"
  
def lines_to_sql_set(txt, xform=lambda txt: txt):
  txt = remove_blank_lines(txt)
  return '(' + ','.join([xform(val) for val in re.split('\r?\n', txt)]) + ')'

def get_current_view_files():
  current_view = notepad.getCurrentView()
  return [file for file in notepad.getFiles() if file[3] == current_view]
