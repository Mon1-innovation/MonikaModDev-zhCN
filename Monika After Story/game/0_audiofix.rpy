# 0.13 更新后需要删除
python early:
    class MASAudioData(unicode):
        """
        NOTE: This is temporal plaster-fix to renpy, use on your own risk,
            this class and all support for it will be completely gone with r8
        NOTE: This DOES NOT support saving in persistent (pickling),
            and it might be unsafe to do so.

        This loads audio from binary data
        """

        def __new__(cls, data, filename):
            rv = unicode.__new__(cls, filename)
            rv.data = data
            return rv

        def __init__(self, data, filename):
            self.filename = filename

        def __reduce__(self):
            # Pickle as a str is safer
            return (str, (self.filename, ))

    renpy.audio.audio.AudioData = MASAudioData
    store.AudioData = MASAudioData
