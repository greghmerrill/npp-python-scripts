# sort all lines alphanumerically and remove duplicates
from sets import Set
editor.setText(''.join(sorted(Set(editor.getText().splitlines(True)))))
editor.gotoLine(0)