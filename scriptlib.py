import re

def remove_blank_lines(txt):
  return re.compile('(^\r?\n)|(\r?\n$)', re.MULTILINE).sub('', txt)

def quote_for_sql(txt):
  return "'" + re.sub('\'', '\'\'', txt) + "'"
  
def lines_to_sql_set(txt, xform=lambda txt: txt):
  txt = remove_blank_lines(txt)
  return '(' + ','.join([xform(val) for val in re.split('\r?\n', txt)]) + ')'
