"""renpy
init -999 python: 
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
        """
        初始化进度条对话框
        :param title: 对话框标题
        :param message: 初始消息
        :param max_value: 进度条最大值 (默认100)
        """
        # 如果不在Android环境，不创建对话框
        if not renpy.android:
            self.dialog = None
            self.progress_bar = None
            self.text_view = None
            return
            
        # 获取必要的 Java 类
        self.PythonSDLActivity = autoclass('org.renpy.android.PythonSDLActivity')
        self.Context = autoclass('android.content.Context')
        self.AlertDialogBuilder = autoclass('android.app.AlertDialog$Builder')
        self.LinearLayout = autoclass('android.widget.LinearLayout')
        self.ProgressBar = autoclass('android.widget.ProgressBar')
        self.TextView = autoclass('android.widget.TextView')
        self.LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        self.WindowManager = autoclass('android.view.WindowManager')
        self.LayoutParamsType = autoclass('android.view.WindowManager$LayoutParams')
        self.Gravity = autoclass('android.view.Gravity')
        
        # 存储参数
        self.title = title
        self.message = message
        self.max_value = max_value
        self.dialog = None
        self.text_view = None
        self.progress_bar = None
        
        # 在 UI 线程上创建对话框
        self._create_dialog()
    
    @run_on_ui_thread
    def _create_dialog(self):
        """创建自定义进度条对话框 (在 UI 线程执行)"""
        try:
            context = self.PythonSDLActivity.mActivity
            
            # 创建垂直布局容器
            layout = self.LinearLayout(context)
            layout.setOrientation(self.LinearLayout.VERTICAL)
            layout.setLayoutParams(self.LayoutParams(
                self.LayoutParams.MATCH_PARENT,
                self.LayoutParams.WRAP_CONTENT
            ))
            
            # 设置适当的间距 (使用dp单位)
            scale = context.getResources().getDisplayMetrics().density
            padding = int(20 * scale)  # 20dp
            layout.setPadding(padding, padding, padding, padding)
            
            # 创建消息文本
            self.text_view = self.TextView(context)
            self.text_view.setText(
                safe_java_string(self.message)
            )
            self.text_view.setTextSize(16)  # 16sp
            layout.addView(self.text_view)
            
            # 添加文本和进度条之间的间距
            spacing = self.TextView(context)
            spacing.setHeight(int(10 * scale))  # 10dp
            layout.addView(spacing)
            
            # 创建水平进度条
            android_R_attr = autoclass('android.R$attr')
            progressBarStyleHorizontal = android_R_attr.progressBarStyleHorizontal
            
            self.progress_bar = self.ProgressBar(
                context, 
                None, 
                progressBarStyleHorizontal
            )
            
            params = self.LayoutParams(
                self.LayoutParams.MATCH_PARENT,
                self.LayoutParams.WRAP_CONTENT
            )
            self.progress_bar.setLayoutParams(params)
            self.progress_bar.setMax(self.max_value)
            self.progress_bar.setProgress(0)
            layout.addView(self.progress_bar)
            
            # 创建对话框
            builder = self.AlertDialogBuilder(context)
            builder.setTitle(safe_java_string(self.title))  # 设置标题)
            builder.setView(layout)
            builder.setCancelable(False)  # 不可取消
            
            self.dialog = builder.create()
            
            # 关键设置：确保对话框显示在游戏上方
            # 使用应用级窗口类型，不需要特殊权限
            self.dialog.getWindow().setType(
                self.LayoutParamsType.TYPE_APPLICATION
            )
            
            # 显示对话框
            self.dialog.show()
            
            # 调试信息
            print("[ProgressDialog] Dialog created and shown")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[ProgressDialog] Error creating dialog: {str(e)}")
    
    @run_on_ui_thread
    def update(self, value, message=None):
        """
        更新进度条
        :param value: 当前进度值 (0-max_value)
        :param message: 更新的消息 (可选)
        """            
        try:
            # 更新进度值
            self.progress_bar.setProgress(value)
            
            # 更新消息文本
            if message and self.text_view:
                self.text_view.setText(
                    safe_java_string(message)
                )

        except Exception as e:
            print(f"[ProgressDialog] Error updating dialog: {str(e)}")
    
    @run_on_ui_thread
    def dismiss(self):
        """关闭对话框"""
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
        """析构时自动关闭对话框"""
        self.dismiss()

def show_progress_example():
    # 创建进度条
    progress = AndroidProgressDialog(
        title="处理中", 
        message="正在加载数据...",
        max_value=100
    )
    
    # 模拟进度更新
    for i in range(1, 101):
        renpy.pause(0.05)  # 短暂暂停
        
        # 每10%更新一次消息
        message = None
        if i % 10 == 0:
            message = f"已完成 {i}%"
        
        progress.update(i, message)
    
    # 完成后关闭
    progress.dismiss()