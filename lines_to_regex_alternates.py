# Converts each line of the active buffer into a single alternation value in a Regular Expression
from scriptlib import *
txt = remove_blank_lines(editor.getText())
new_txt = '(' + ')|('.join([val for val in re.split('\r?\n', txt)]) + ')'
editor.setText(new_txt)
