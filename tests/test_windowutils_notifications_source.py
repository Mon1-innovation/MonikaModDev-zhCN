from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
