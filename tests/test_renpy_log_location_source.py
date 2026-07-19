from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RENpy_DIR = ROOT / "Monika After Story" / "renpy"


class RenpyLogLocationSourceTests(unittest.TestCase):

    def test_bootstrap_prefers_log_subdirectory_for_logdir(self):
        source = (RENpy_DIR / "bootstrap.py").read_text(encoding="utf-8")

        self.assertIn("def choose_logdir(preferred, fallback):", source)
        self.assertIn('test_fn = os.path.join(path, ".renpy-log-test")', source)
        self.assertIn("return fallback", source)
        self.assertIn('base_logdir = "/storage/emulated/0/MAS"', source)
        self.assertIn("default_logdir = os.environ['ANDROID_PUBLIC']", source)
        self.assertIn("base_logdir = basedir", source)
        self.assertIn("default_logdir = basedir", source)
        self.assertIn(
            'renpy.config.logdir = choose_logdir(os.path.join(base_logdir, "log"), default_logdir)',
            source
        )
        self.assertNotIn("renpy.config.logdir = os.environ['ANDROID_PUBLIC']", source)
        self.assertNotIn("renpy.config.logdir = basedir", source)

    def test_mobile_logdir_falls_back_to_default_android_public_when_mas_log_unwritable(self):
        source = (ROOT / "Monika After Story" / "game" / "0mobile.rpy").read_text(encoding="utf-8")

        self.assertIn("def choose_android_logdir(preferred, fallback):", source)
        self.assertIn('test_fn = os.path.join(path, ".mas-log-test")', source)
        self.assertIn("return fallback", source)
        self.assertIn("android_default_logdir = os.environ.get('ANDROID_PUBLIC', ANDROID_MASBASE)", source)
        self.assertIn(
            'renpy.config.logdir = choose_android_logdir(os.path.join(ANDROID_MASBASE, "log"), android_default_logdir)',
            source
        )

    def test_mobile_no_longer_copies_error_logs_after_report_exception(self):
        source = (ROOT / "Monika After Story" / "game" / "0mobile.rpy").read_text(encoding="utf-8")

        self.assertNotIn("def _error_copyer", source)
        self.assertNotIn("_error_copyer()", source)
        self.assertIn("original_report_exception = renpy.renpy.error.report_exception", source)

    def test_mobile_android_exception_handler_shows_log_toast_and_waits_on_init_dialog(self):
        source = (ROOT / "Monika After Story" / "game" / "0mobile.rpy").read_text(encoding="utf-8")
        handler_source = source[
            source.index("    def new_report_exception"):
            source.index("    renpy.renpy.error.report_exception = new_report_exception")
        ]

        self.assertIn('android_toast("x_x 游戏崩溃了, 请查看log文件夹以获取详细信息")', handler_source)
        self.assertIn("AndroidAlertDialog", handler_source)
        self.assertIn("将在10秒后自动退出", handler_source)
        self.assertIn("window.AsyncTaskerCheck.wait()", handler_source)
        self.assertNotIn("AndroidClipboard().copy_to_clipboard(res[1])", handler_source)
        self.assertNotIn("报错堆栈已复制到剪贴板", handler_source)


if __name__ == "__main__":
    unittest.main()
