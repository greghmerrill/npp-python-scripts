# sort all lines by length
editor.setText(''.join(sorted(editor.getText().splitlines(True), key=len)))
editor.gotoLine(0)