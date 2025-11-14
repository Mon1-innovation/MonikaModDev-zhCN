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
import time
class AndroidAlertDialog:
    
    MAX_WAITTIME = 10
    def __init__(self, title, message, positive_text="确定", negative_text="取消"):
        self.title = title
        self.message = message
        self.positive_text = positive_text
        self.negative_text = negative_text
        self.result = None  # Python 回调函数，参数是 True / False
        self.finished = False
        self.dialog = None
        self._create_dialog()
        self.AsyncTaskerCheck = AsyncTask(self.checker)
        self.starttime = time.time()

    def checker(self):
        """检查对话框是否已完成"""
        while not self.finished:
            time.sleep(0.1)
            if (time.time()-self.starttime) > self.MAX_WAITTIME:
                break
        return True
        
    @run_on_ui_thread
    def _create_dialog(self):
        try:
            # 引入Java类
            PythonSDLActivity = autoclass('org.renpy.android.PythonSDLActivity')
            LinearLayout = autoclass('android.widget.LinearLayout')
            TextView = autoclass('android.widget.TextView')
            ScrollView = autoclass('android.widget.ScrollView')
            Button = autoclass('android.widget.Button')
            GradientDrawable = autoclass('android.graphics.drawable.GradientDrawable')
            Color = autoclass('android.graphics.Color')
            Dialog = autoclass('android.app.Dialog')
            Gravity = autoclass('android.view.Gravity')
            LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
            WindowManagerLayoutParams = autoclass('android.view.WindowManager$LayoutParams')
            ColorDrawable = autoclass('android.graphics.drawable.ColorDrawable')

            context = PythonSDLActivity.mActivity
            scale = context.getResources().getDisplayMetrics().density

            # 主布局
            main_layout = LinearLayout(context)
            main_layout.setOrientation(LinearLayout.VERTICAL)
            main_layout.setPadding(int(24 * scale), int(24 * scale), int(24 * scale), int(16 * scale))
            main_layout.setGravity(Gravity.CENTER_HORIZONTAL)

            background = GradientDrawable()
            background.setColor(Color.WHITE)
            background.setCornerRadius(12 * scale)
            main_layout.setBackground(background)

            # 标题
            title_view = TextView(context)
            title_view.setText(safe_java_string(self.title))
            title_view.setTextSize(20)
            title_view.setTextColor(Color.BLACK)
            title_view.setPadding(0, 0, 0, int(12 * scale))
            title_view.setTypeface(None, 1)  # BOLD
            main_layout.addView(title_view)

            # Scrollable 内容
            scroll = ScrollView(context)
            scroll_params = LayoutParams(LayoutParams.MATCH_PARENT, int(200 * scale))
            scroll.setLayoutParams(scroll_params)

            msg_container = LinearLayout(context)
            msg_container.setOrientation(LinearLayout.VERTICAL)

            message_view = TextView(context)
            message_view.setText(safe_java_string(self.message))
            message_view.setTextSize(16)
            message_view.setTextColor(Color.DKGRAY)
            message_view.setLineSpacing(0, 1.2)
            msg_container.addView(message_view)

            scroll.addView(msg_container)
            main_layout.addView(scroll)

            # 按钮布局
            btn_layout = LinearLayout(context)
            btn_layout.setOrientation(LinearLayout.HORIZONTAL)
            btn_layout.setGravity(Gravity.END)
            btn_layout.setPadding(0, int(12 * scale), 0, 0)

            # Negative 按钮
            neg_button = Button(context)
            neg_button.setText(safe_java_string(self.negative_text))
            neg_button.setTextColor(Color.parseColor("#F44336"))  # Material Red
            neg_button.setBackgroundColor(Color.TRANSPARENT)
            neg_button.setOnClickListener(OnClickListener(lambda: self._handle_result(False)))
            btn_layout.addView(neg_button)

            # Spacing
            spacer = TextView(context)
            spacer.setWidth(int(16 * scale))
            btn_layout.addView(spacer)

            # Positive 按钮
            pos_button = Button(context)
            pos_button.setText(safe_java_string(self.positive_text))
            pos_button.setTextColor(Color.parseColor("#2196F3"))  # Material Blue
            pos_button.setBackgroundColor(Color.TRANSPARENT)
            pos_button.setOnClickListener(OnClickListener(lambda: self._handle_result(True)))
            btn_layout.addView(pos_button)

            main_layout.addView(btn_layout)

            # Dialog 显示
            self.dialog = Dialog(context)
            self.dialog.setContentView(main_layout)
            self.dialog.setCancelable(False)

            window = self.dialog.getWindow()
            window.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
            window.setLayout(int(600 * scale), WindowManagerLayoutParams.WRAP_CONTENT)
            window.setType(WindowManagerLayoutParams.TYPE_APPLICATION)

            self.dialog.show()
            print("[AlertDialog] Custom dialog shown")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[AlertDialog] Error: {str(e)}")
    
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
    )
    return d.result  # 返回对话框结果，True 或 False