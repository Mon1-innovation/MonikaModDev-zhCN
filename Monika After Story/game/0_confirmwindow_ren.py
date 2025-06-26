"""renpy
init python early: 
    if renpy.android:
        pass
"""

from jnius import autoclass, PythonJavaClass, java_method, cast
from android_runnable import run_on_ui_thread

import six

def safe_java_string(py_str):
    if isinstance(py_str, six.text_type):
        jstr = autoclass('java.lang.String')(py_str.encode('utf-16-le'), 'utf-16-le')
    else:
        jstr = autoclass('java.lang.String')(py_str, 'utf-8')
    return cast('java.lang.CharSequence', jstr)

# 定义按钮回调接口（用于监听按钮点击）
class OnClickListener(PythonJavaClass):
    __javainterfaces__ = ['android.content.DialogInterface$OnClickListener']
    __javacontext__ = 'app'

    def __init__(self, callback):
        super(OnClickListener, self).__init__()
        self.callback = callback

    @java_method('(Landroid/content/DialogInterface;I)V')
    def onClick(self, dialog, which):
        self.callback(which)

class AndroidAlertDialog:
    def __init__(self, title, message, positive_text="确定", negative_text="取消", on_result=None):
        self.title = title
        self.message = message
        self.positive_text = positive_text
        self.negative_text = negative_text
        self.result = None  # Python 回调函数，参数是 True / False
        self.finished = False
        self.dialog = None
        self._create_dialog()

    @run_on_ui_thread
    def _create_dialog(self):
        try:
            AlertDialogBuilder = autoclass('android.app.AlertDialog$Builder')
            PythonSDLActivity = autoclass('org.renpy.android.PythonSDLActivity')
            context = PythonSDLActivity.mActivity

            # 创建 AlertDialog.Builder 实例
            builder = AlertDialogBuilder(context)
            builder.setTitle(safe_java_string(self.title))
            builder.setMessage(safe_java_string(self.message))

            # 设置按钮及其监听器
            builder.setPositiveButton(safe_java_string(self.positive_text),
                                      OnClickListener(lambda which: self._handle_result(True)))
            builder.setNegativeButton(safe_java_string(self.negative_text),
                                      OnClickListener(lambda which: self._handle_result(False)))

            # 创建并显示对话框
            self.dialog = builder.create()
            self.dialog.setCancelable(False)  # 不允许点击外部取消
            self.dialog.show()

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[AlertDialog] Error: {e}")

    @run_on_ui_thread
    def dismiss(self):
        if self.dialog and self.dialog.isShowing():
            self.dialog.dismiss()
            self.dialog = None

    def _handle_result(self, result):
        self.dismiss()
        self.result = result
        self.finished = True

# 示例调用
def show_alert_dialog_example():
    def result_handler(result):
        print("用户选择了：", "是" if result else "否")
    text = """\
I'm sorry, but errors were detected in your script. Please correct the
errors listed below, and try again.


File "game/Submods/MAICA_MTTSubmod/header.rpy", line 70: textbutton expects a non-empty block.
    textbutton "[persistent.mtts.get('volume')]":
                                                 ^

Ren'Py Version: Ren'Py 6.99.12.4.2187
"""
    d = AndroidAlertDialog(
        title="操作确认",
        message=text,
        positive_text="是的",
        negative_text="取消",
        on_result=result_handler
    )
    return d.result  # 返回对话框结果，True 或 False