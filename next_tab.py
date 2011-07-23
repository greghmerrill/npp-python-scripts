# While the Notepad++ "Switch to previous/next document" actions are useful, I personally like
# to bind Ctrl+PageUp/PageDn to switch to the tab which appears next/prev in the tab list.
# next_tab.py and prev_tab.py provide this capability.  (Use Python Script's "Configuration" to add
# these as Menu Items, then you can map them with the Notepad++ Shortcut Mapper.)
from scriptlib import *
new_index = notepad.getCurrentDocIndex(notepad.getCurrentView()) + 1
notepad.activateIndex(0, new_index if len(get_current_view_files()) > new_index else 0)
