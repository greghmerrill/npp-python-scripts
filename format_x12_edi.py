# re-format the given editor content as readable X12 EDI by changing the segment delimiter to \n
import re
delim = editor.getText()[105]
editor.setText(re.sub(re.escape(delim), '\n', editor.getText()))
editor.gotoLine(0)
