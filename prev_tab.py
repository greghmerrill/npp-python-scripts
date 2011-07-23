# See next_tab.py for details ...
from scriptlib import *
new_index = notepad.getCurrentDocIndex(notepad.getCurrentView()) - 1
notepad.activateIndex(0, new_index if new_index >= 0 else len(get_current_view_files()) - 1)
