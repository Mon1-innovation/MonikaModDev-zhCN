from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DIALOG_SOURCE = ROOT / "Monika After Story" / "game" / "0_confirmwindow_ren.py"


class AndroidAlertDialogSourceTests(unittest.TestCase):

    def test_alert_dialog_sizes_to_screen_and_keeps_actions_outside_scroll(self):
        source = DIALOG_SOURCE.read_text(encoding="utf-8")

        self.assertIn("display_metrics = context.getResources().getDisplayMetrics()", source)
        self.assertIn("dialog_width = int(display_metrics.widthPixels * 0.92)", source)
        self.assertIn("max_scroll_height = int(display_metrics.heightPixels * 0.58)", source)
        self.assertIn("scroll_params = LayoutParams(LayoutParams.MATCH_PARENT, max_scroll_height)", source)
        self.assertIn("window.setLayout(dialog_width, WindowManagerLayoutParams.WRAP_CONTENT)", source)
        self.assertNotIn("window.setLayout(int(600 * scale)", source)
        self.assertNotIn("int(200 * scale)", source)

        scroll_block = source[source.index("# Scrollable 内容"):source.index("main_layout.addView(scroll)")]
        button_block = source[source.index("# 按钮布局"):source.index("main_layout.addView(btn_layout)")]

        self.assertIn("scroll.setFillViewport(False)", scroll_block)
        self.assertIn("btn_layout", button_block)
        self.assertNotIn("btn_layout", scroll_block)


if __name__ == "__main__":
    unittest.main()
