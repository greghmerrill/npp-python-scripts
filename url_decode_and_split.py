# Takes a URL, splits each URL param into a different line, and performs a URL decode on each
import re, urllib
text = urllib.unquote(editor.getText()).decode('UTF-8')
text = re.sub('([&])', r'\n\1', text)
editor.setText(text)
