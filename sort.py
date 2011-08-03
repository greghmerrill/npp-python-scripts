# sort all lines alphanumerically
editor.setText(''.join(sorted(editor.getText().splitlines(True))))
editor.gotoLine(0)