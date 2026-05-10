from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
JAVA_SOURCE_DIR = ROOT / "docs" / "android-notification-java-source"


def read_java_file(name):
    return (JAVA_SOURCE_DIR / name).read_text(encoding="utf-8")


class AndroidNotificationJavaSourceTests(unittest.TestCase):

    def test_notification_helper_uses_conversation_notification_layout(self):
        source = read_java_file("NotificationHelper.java")

        self.assertIn("NotificationCompat.MessagingStyle", source)
        self.assertIn('getIdentifier("monika_contact_icon", "drawable"', source)
        self.assertIn('getIdentifier("icon", "mipmap"', source)
        self.assertIn("ShortcutInfoCompat", source)
        self.assertIn("ShortcutManagerCompat.pushDynamicShortcut", source)
        self.assertIn('builder.setShortcutId("monika_chat_shortcut")', source)
        self.assertIn('"android.shortcut.conversation"', source)

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


if __name__ == "__main__":
    unittest.main()
