# Elimintes end-of-line characters to join all lines on the current page into a single line
import re
newText = re.compile('\r?\n', re.MULTILINE).sub('', editor.getText())
editor.setText(newText)
