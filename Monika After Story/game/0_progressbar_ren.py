"""renpy
init python early: 
    if renpy.android:
        pass
"""
from jnius import autoclass, cast
from android_runnable import run_on_ui_thread

import six  # 用于处理Python 2/3兼容性

# 创建安全的Java字符串
def safe_java_string(py_str):
    # 处理可能的代理对问题
    if isinstance(py_str, six.text_type):
        # 使用UTF-16编码处理代理对
        jstr = autoclass('java.lang.String')(py_str.encode('utf-16-le'), 'utf-16-le')
    else:
        # 如果是字节串则直接解码
        jstr = autoclass('java.lang.String')(py_str, 'utf-8')
    return cast('java.lang.CharSequence', jstr)

class AndroidProgressDialog:
    def __init__(self, title, message, max_value=100):
        if not renpy.android:
            self.dialog = None
            self.progress_bar = None
            self.text_view = None
            return

        # Java 类初始化
        self.PythonSDLActivity = autoclass('org.renpy.android.PythonSDLActivity')
        self.LinearLayout = autoclass('android.widget.LinearLayout')
        self.ProgressBar = autoclass('android.widget.ProgressBar')
        self.TextView = autoclass('android.widget.TextView')
        self.LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        self.Gravity = autoclass('android.view.Gravity')
        self.GradientDrawable = autoclass('android.graphics.drawable.GradientDrawable')
        self.Color = autoclass('android.graphics.Color')
        self.ClipDrawable = autoclass("android.graphics.drawable.ClipDrawable")
        self.Dialog = autoclass("android.app.Dialog")
        self.ColorDrawable = autoclass("android.graphics.drawable.ColorDrawable")
        self.LayoutParamsType = autoclass("android.view.WindowManager$LayoutParams")
        self.android_R_attr = autoclass("android.R$attr")

        # 存储参数
        self.title = title
        self.message = message
        self.max_value = max_value
        self.dialog = None
        self.text_view = None
        self.title_view = None
        self.progress_bar = None

        self._create_dialog()

    @run_on_ui_thread
    def _create_dialog(self):
        try:
            context = self.PythonSDLActivity.mActivity
            scale = context.getResources().getDisplayMetrics().density

            # 主布局
            layout = self.LinearLayout(context)
            layout.setOrientation(self.LinearLayout.VERTICAL)
            layout.setGravity(self.Gravity.CENTER_HORIZONTAL)
            layout.setLayoutParams(self.LayoutParams(
                self.LayoutParams.MATCH_PARENT,
                self.LayoutParams.WRAP_CONTENT
            ))

            padding = int(24 * scale)
            layout.setPadding(padding, padding, padding, padding)

            # 设置圆角背景
            background = self.GradientDrawable()
            background.setColor(self.Color.WHITE)
            background.setCornerRadius(12 * scale)
            layout.setBackground(background)

            # 自定义标题
            self.title_view = self.TextView(context)
            self.title_view.setText(safe_java_string(self.title))
            self.title_view.setTextSize(20)
            self.title_view.setTextColor(self.Color.BLACK)
            self.title_view.setTypeface(None, 1)  # BOLD
            self.title_view.setPadding(0, 0, 0, int(12 * scale))
            layout.addView(self.title_view)

            # 消息文本
            self.text_view = self.TextView(context)
            self.text_view.setText(safe_java_string(self.message))
            self.text_view.setTextSize(18)
            self.text_view.setTextColor(self.Color.BLACK)
            self.text_view.setTypeface(None, 1)  # BOLD
            layout.addView(self.text_view)

            # 间距
            spacing = self.TextView(context)
            spacing.setHeight(int(12 * scale))
            layout.addView(spacing)

            # 水平进度条
            progressBarStyleHorizontal = self.android_R_attr.progressBarStyleHorizontal
            self.progress_bar = self.ProgressBar(context, None, progressBarStyleHorizontal)

            params = self.LayoutParams(
                self.LayoutParams.MATCH_PARENT,
                int(8 * scale)
            )
            self.progress_bar.setLayoutParams(params)
            self.progress_bar.setMax(self.max_value)
            self.progress_bar.setProgress(0)

            # 扁平蓝色进度条
            progress_drawable = self.GradientDrawable()
            progress_drawable.setShape(self.GradientDrawable.RECTANGLE)
            progress_drawable.setColor(self.Color.parseColor("#2196F3"))  # Material Blue
            progress_drawable.setCornerRadius(4 * scale)

            clip = self.ClipDrawable(progress_drawable, self.Gravity.START, self.ClipDrawable.HORIZONTAL)
            self.progress_bar.setProgressDrawable(clip)
            self.progress_bar.setBackgroundColor(self.Color.parseColor("#E0E0E0"))  # 浅灰背景

            layout.addView(self.progress_bar)

            # 使用 Dialog（非 AlertDialog）创建对话框
            self.dialog = self.Dialog(context)
            self.dialog.setContentView(layout)
            self.dialog.setCancelable(False)

            # 设置透明背景（移除黑框）
            window = self.dialog.getWindow()
            window.setBackgroundDrawable(self.ColorDrawable(self.Color.TRANSPARENT))
            window.setLayout(int(600 * scale), self.LayoutParams.WRAP_CONTENT)
            window.setType(self.LayoutParamsType.TYPE_APPLICATION)

            self.dialog.show()
            print("[ProgressDialog] Dialog created and shown")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[ProgressDialog] Error creating dialog: {str(e)}")

    @run_on_ui_thread
    def update(self, value, message=None, title=None):
        try:
            self.progress_bar.setProgress(value)
            if message and self.text_view:
                self.text_view.setText(safe_java_string(message))
            if title and self.title_view:
                self.dialog.setTitle(safe_java_string(title))
        except Exception as e:
            print(f"[ProgressDialog] Error updating dialog: {str(e)}")

    @run_on_ui_thread
    def dismiss(self):
        if not renpy.android or not self.dialog:
            return
        try:
            if self.dialog.isShowing():
                self.dialog.dismiss()
                print("[ProgressDialog] Dialog dismissed")
            self.dialog = None
            self.progress_bar = None
            self.text_view = None
        except Exception as e:
            print(f"[ProgressDialog] Error dismissing dialog: {str(e)}")

    def __del__(self):
        self.dismiss()

def show_progress_example():
    # 创建进度条
    progress = AndroidProgressDialog(
        title="处理中", 
        message="正在加载数据...",
        max_value=100
    )
    import time
    # 模拟进度更新
    for i in range(1, 101):
          # 短暂暂停
        time.sleep(0.03)
        # 每10%更新一次消息
        message = None
        if i % 10 == 0:
            message = f"已完成 {i}%"
        
        progress.update(i, message)
    
    # 完成后关闭
    progress.dismiss()