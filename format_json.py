from json import *
editor.setText(dumps(loads(editor.getText()), indent=2))
editor.gotoLine(0)
