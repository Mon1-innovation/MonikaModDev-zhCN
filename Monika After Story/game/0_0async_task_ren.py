"""renpy
python early: 
"""
import threading


class AsyncTask(object):
    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self.result = None
        self.exception = None
        self.is_finished = False
        self.is_success = False

        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def _run(self):
        try:
            self.result = self._func(*self._args, **self._kwargs)
            self.is_success = True
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.exception = e
            self.is_success = False

        finally:
            self.is_finished = True

    @property
    def is_alive(self):
        return self._thread.is_alive()

    def wait(self, timeout=None):
        self._thread.join(timeout=timeout)
