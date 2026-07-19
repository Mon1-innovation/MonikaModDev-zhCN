"""renpy
init python early:
    if renpy.android:
        pass
"""

from jnius import autoclass
import time
from android_runnable import run_on_ui_thread
class AndroidImageSelector:
    MAX_WAITTIME = 60

    def __init__(self):
        if not renpy.android:
            return

        self.PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
        self.SelectImage = autoclass('org.renpy.android.select_image')
        self.starttime = time.time()

        activity = self.PythonActivity.mActivity
        self._start_selector(activity)

    @run_on_ui_thread
    def _start_selector(self, activity):
        self.SelectImage.selectImage(activity)
    
    @property
    def image_path(self):
        return self.SelectImage.getImagePath()
    
    @property
    def is_selecting(self):
        return self.SelectImage.isSelecting()
def select_image():
    if not renpy.android:
        return None
    selector = AndroidImageSelector()
    return selector
