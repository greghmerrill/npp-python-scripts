# delete all content except for html form elements like form, input, select
import re
matches = re.compile('<form.*?>|<input.*?>|<select.*?>', re.DOTALL).findall(editor.getText())
editor.setText('\n'.join(re.sub('\r?\n', ' ', match) for match in matches))
