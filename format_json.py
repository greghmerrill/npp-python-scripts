import json
try:
  editor.setText(json.dumps(json.loads(editor.getText()), indent=2))
  editor.gotoLine(0)
except Exception as e:
  console.show()
  console.write(str(e) + '\r\n')
