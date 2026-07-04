from pathlib import Path
import ast
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
WINDOWUTILS_RPY = ROOT / "Monika After Story" / "game" / "zz_windowutils.rpy"


class WindowUtilsNotificationSourceTests(unittest.TestCase):

    def test_test_notifications_log_failures_to_mas_log(self):
        source = WINDOWUTILS_RPY.read_text(encoding="utf-8")
        function_source = source[
            source.index("    def mas_display_notif("):
            source.index("    def mas_isFocused():")
        ]

        self.assertIn("def _log_test_notif_failure", function_source)
        self.assertIn("if skip_checks:", function_source)
        self.assertIn("store.mas_utils.mas_log.error", function_source)
        self.assertIn("mas_display_notif: test notification failed", function_source)
        self.assertIn("android display backend returned False", function_source)
        self.assertIn("desktop display backend returned False", function_source)

    def test_display_notif_group_defaults_to_none_for_test_notifications(self):
        source = WINDOWUTILS_RPY.read_text(encoding="utf-8")
        function_source = source[
            source.index("    def mas_display_notif("):
            source.index("    def mas_isFocused():")
        ]
        module = ast.parse(textwrap.dedent(function_source))
        display_notif = next(
            node for node in ast.walk(module)
            if isinstance(node, ast.FunctionDef)
            and node.name == "mas_display_notif"
        )

        group_arg_index = next(
            index for index, arg in enumerate(display_notif.args.args)
            if arg.arg == "group"
        )
        defaults_offset = len(display_notif.args.args) - len(display_notif.args.defaults)
        group_default = display_notif.args.defaults[group_arg_index - defaults_offset]

        self.assertIsInstance(group_default, ast.Constant)
        self.assertIsNone(group_default.value)

    def test_android_try_show_notification_delegates_to_android_backend(self):
        source = WINDOWUTILS_RPY.read_text(encoding="utf-8")
        function_source = source[
            source.index("    def _tryShowNotification_Android("):
            source.index("    #Mouse Position related funcs")
        ]

        self.assertIn('hasattr(store, "mas_android_display_notif")', function_source)
        self.assertIn("return store.mas_android_display_notif(title, body)", function_source)
        self.assertIn("return False", function_source)


if __name__ == "__main__":
    unittest.main()
