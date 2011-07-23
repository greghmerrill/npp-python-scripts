from scriptlib import *
new_index = notepad.getCurrentDocIndex(notepad.getCurrentView()) + 1
notepad.activateIndex(0, new_index if len(get_current_view_files()) > new_index else 0)
