from pathlib import Path
import types
import unittest


ROOT = Path(__file__).resolve().parents[1]
DIALOG_SOURCE = ROOT / "Monika After Story" / "game" / "0_confirmwindow_ren.py"


class AndroidAlertDialogSourceTests(unittest.TestCase):

    def test_alert_dialog_sizes_to_landscape_screen_and_keeps_actions_visible(self):
        source = DIALOG_SOURCE.read_text(encoding="utf-8")

        self.assertIn("display_metrics = context.getResources().getDisplayMetrics()", source)
        self.assertIn("dialog_width = min(int(short_side * 1.72), int(long_side * 0.92))", source)
        self.assertIn("max_scroll_height = int(short_side * 0.34)", source)
        self.assertIn("scroll_height = _estimate_alert_scroll_height(", source)
        self.assertIn("window.setGravity(Gravity.CENTER)", source)
        self.assertIn("window.setLayout(dialog_width, WindowManagerLayoutParams.WRAP_CONTENT)", source)
        self.assertNotIn("window.setLayout(int(600 * scale)", source)
        self.assertNotIn("int(200 * scale)", source)

        scroll_block = source[source.index("# Scrollable 内容"):source.index("main_layout.addView(scroll)")]
        button_block = source[source.index("# 按钮布局"):source.index("main_layout.addView(btn_layout)")]

        self.assertIn("scroll.setFillViewport(False)", scroll_block)
        self.assertIn("btn_layout", button_block)
        self.assertIn("btn_layout.setLayoutParams(LayoutParams(", button_block)
        self.assertIn("LayoutParams.MATCH_PARENT", button_block)
        self.assertNotIn("btn_layout", scroll_block)

    def test_alert_dialog_uses_button_view_listener(self):
        source = DIALOG_SOURCE.read_text(encoding="utf-8")

        self.assertIn("android.view.View$OnClickListener", source)
        self.assertIn("@java_method('(Landroid/view/View;)V')", source)
        self.assertNotIn("android.content.DialogInterface$OnClickListener", source)

    def test_alert_dialog_hides_empty_action_buttons(self):
        source = DIALOG_SOURCE.read_text(encoding="utf-8")

        self.assertIn("if self.negative_text:", source)
        self.assertIn("if self.positive_text:", source)
        self.assertIn("if has_buttons:", source)
        self.assertIn("main_layout.addView(btn_layout)", source)

    def test_alert_scroll_height_estimate_keeps_short_errors_compact(self):
        source = DIALOG_SOURCE.read_text(encoding="utf-8")

        namespace = {}
        function_source = source[
            source.index("def _estimate_alert_scroll_height"):
            source.index("\n# 定义按钮回调接口")
        ]
        self.assertIn("six.text_type", function_source)
        namespace["six"] = types.SimpleNamespace(text_type=str)
        exec(function_source, namespace)

        estimate = namespace["_estimate_alert_scroll_height"]
        short_message = "While loading the script.\nFile \"game/0utils.rpy\", line 373\nException"
        long_message = "\n".join("Trace line {}".format(i) for i in range(80))

        self.assertLess(estimate(short_message, 900, 2.0), 260)
        self.assertEqual(estimate(long_message, 900, 2.0), int(900 * 0.34))


if __name__ == "__main__":
    unittest.main()
