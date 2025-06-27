from jnius import autoclass, cast
from android_runnable import run_on_ui_thread

class AndroidClipboard:
    def __init__(self):
        # 获取当前 Android 活动上下文
        PythonSDLActivity = autoclass('org.renpy.android.PythonSDLActivity')
        self.context = PythonSDLActivity.mActivity
        self.ClipboardManager = autoclass('android.content.ClipboardManager')
        self.ClipData = autoclass('android.content.ClipData')

        # 获取系统剪贴板服务
        self.clipboard = cast('android.content.ClipboardManager',
                              self.context.getSystemService(self.context.CLIPBOARD_SERVICE))

    @run_on_ui_thread
    def copy_to_clipboard(self, text):
        """复制文本到剪贴板"""
        clip = self.ClipData.newPlainText("label", text)
        self.clipboard.setPrimaryClip(clip)

    def get_from_clipboard(self):
        """从剪贴板读取文本"""
        if self.clipboard.hasPrimaryClip():
            clipData = self.clipboard.getPrimaryClip()
            item = clipData.getItemAt(0)
            text = item.getText()
            if text is not None:
                return str(text)
        return ""

# 示例使用
def example_clipboard_usage():
    clipboard = AndroidClipboard()
    
    # 复制
    clipboard.copy_to_clipboard("这是测试文本")
    
    # 粘贴
    pasted_text = clipboard.get_from_clipboard()
    print("从剪贴板读取的内容是：", pasted_text)