from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
JAVA_SOURCE_DIR = ROOT / "docs" / "android-notification-java-source"


def read_java_file(name):
    return (JAVA_SOURCE_DIR / name).read_text(encoding="utf-8")


class AndroidNotificationJavaSourceTests(unittest.TestCase):

    def test_notification_helper_uses_xiaomi_native_large_icon_layout(self):
        source = read_java_file("NotificationHelper.java")

        self.assertIn("NotificationCompat.BigTextStyle", source)
        self.assertIn(".bigText(message)", source)
        self.assertIn(".setContentTitle(title)", source)
        self.assertIn(".setContentText(message)", source)
        self.assertIn('getIdentifier("monika_contact_icon", "drawable"', source)
        self.assertIn('getIdentifier("icon", "mipmap"', source)
        self.assertIn("builder.setLargeIcon(circularBitmap)", source)
        self.assertNotIn("NotificationCompat.MessagingStyle", source)
        self.assertNotIn("new Person.Builder()", source)
        self.assertNotIn("ShortcutInfoCompat", source)
        self.assertNotIn("ShortcutManagerCompat.pushDynamicShortcut", source)
        self.assertNotIn("setShortcutId", source)
        self.assertNotIn('"android.shortcut.conversation"', source)

    def test_notification_helper_uses_v7_to_v10_channel_architecture(self):
        source = read_java_file("NotificationHelper.java")

        self.assertIn('CHANNEL_GROUP_ID = "mas_group"', source)
        self.assertIn('CHANNEL_ID_INTERACTIVE = "mas_v7"', source)
        self.assertIn('CHANNEL_ID_BIRTHDAY = "mas_v8"', source)
        self.assertIn('CHANNEL_ID_RANDOM = "mas_v9"', source)
        self.assertIn('CHANNEL_ID_SPECIAL = "mas_v10"', source)
        self.assertIn("new NotificationChannelGroup", source)
        self.assertIn("deleteNotificationChannel", source)
        self.assertIn("Locale.getDefault().getLanguage()", source)

    def test_telemetry_logger_writes_monitor_log_under_log_directory(self):
        source = read_java_file("TelemetryLogger.java")

        self.assertIn('new File("/storage/emulated/0/MAS/log")', source)
        self.assertIn('new File(baseDir, "log")', source)
        self.assertIn("if (!dir.exists() && !dir.mkdirs())", source)
        self.assertIn('new File(dir, "tec_android_monitor.txt")', source)
        self.assertLess(
            source.index('new File("/storage/emulated/0/MAS/log")'),
            source.index('new File(baseDir, "log")')
        )


if __name__ == "__main__":
    unittest.main()
