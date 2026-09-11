"""renpy
init python early: 
    if renpy.android:
        pass
"""

from jnius import autoclass

class AndroidClipboard:
    def __init__(self):
        # Reuse Ren'Py's initialized SDL clipboard bridge.
        self._sdl_activity = autoclass("org.libsdl.app.SDLActivity")

    def copy_to_clipboard(self, text):
        """Copies text to the Android clipboard."""
        try:
            self._sdl_activity.clipboardSetText(str(text))
            return True
        except Exception as e:
            print("[MAS_CLIPBOARD] Copy failed: " + str(e))
            return False

    def get_from_clipboard(self):
        """Returns clipboard text, or an empty string when it is unavailable."""
        try:
            text = self._sdl_activity.clipboardGetText()
            return "" if text is None else str(text)
        except Exception as e:
            print("[MAS_CLIPBOARD] Read failed: " + str(e))
            return ""
