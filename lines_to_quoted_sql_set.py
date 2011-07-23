# Converts each line of the active buffer into a single string in a SQL Set suitable for use with an "IN" clause.
from scriptlib import *
editor.setText(lines_to_sql_set(editor.getText(), quote_for_sql))
