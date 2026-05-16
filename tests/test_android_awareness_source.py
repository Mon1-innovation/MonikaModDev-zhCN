from pathlib import Path
import ast
import re
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "Monika After Story" / "game"
AWARENESS_RPY = GAME_DIR / "zz_android_awareness.rpy"
RAPT_MAIN = Path("J:/Renpy/renpy-8.2.3-sdk/rapt/project/app/src/main")
RAPT_JAVA = RAPT_MAIN / "java" / "com" / "monikaafterstory" / "tec" / "es" / "AwarenessService.java"
RAPT_MANIFEST = RAPT_MAIN / "AndroidManifest.xml"
RAPT_TEMPLATE_MANIFEST = Path("J:/Renpy/renpy-8.2.3-sdk/rapt/templates/app-AndroidManifest.xml")


def read_text(path):
    return path.read_text(encoding="utf-8")


def extract_init_python_block(source, label):
    lines = source.splitlines()
    start = next(index for index, line in enumerate(lines) if line.startswith(label)) + 1
    for index in range(start, len(lines)):
        if lines[index].startswith("init ") or lines[index].startswith("label ") or lines[index].startswith("screen "):
            return lines[start:index]
    return lines[start:]


class AndroidAwarenessSourceTests(unittest.TestCase):

    def test_awareness_module_defines_snapshot_bridge_and_reaction_helpers(self):
        source = read_text(AWARENESS_RPY)

        self.assertIn('"/storage/emulated/0/Monika After Story/log/.awareness"', source)
        self.assertIn("def mas_awareness_read_snapshot", source)
        self.assertIn("def mas_awareness_get_most_recent_app", source)
        self.assertIn("def mas_awareness_get_app_category", source)
        self.assertIn("def mas_awareness_get_app_reaction", source)
        self.assertIn("def mas_awareness_request_usage_permission", source)
        self.assertIn("def mas_awareness_force_snapshot", source)
        self.assertIn("store.mas_awareness_get_app_reaction", source)
        self.assertIn("persistent._mas_awareness_enabled", source)
        self.assertIn("persistent._mas_awareness_last_app_mention", source)

    def test_awareness_init_blocks_are_valid_python(self):
        source = read_text(AWARENESS_RPY)

        for label in (
            "init -10 python:",
            "init -5 python:",
            "init 5 python:",
            "init 10 python:",
        ):
            block = textwrap.dedent("\n".join(extract_init_python_block(source, label)))
            ast.parse(block)

    def test_awareness_settings_are_exposed_in_android_notifications_screen(self):
        source = read_text(GAME_DIR / "screens.rpy")
        notif_screen = source[source.index("screen notif_settings():"):]

        self.assertIn('textbutton _("Awareness")', notif_screen)
        self.assertIn('textbutton _("Permits")', notif_screen)
        self.assertIn('Show("mas_awareness_permits_confirm")', notif_screen)
        self.assertIn("persistent._mas_awareness_enabled", notif_screen)
        self.assertIn("layout.MAS_TT_ANDROID_AWARENESS", source)
        self.assertIn("layout.MAS_TT_ANDROID_AWARENESS_PERMITS", source)

    def test_awareness_java_source_uses_usage_stats_and_existing_notification_helper(self):
        source = read_text(RAPT_JAVA)

        self.assertIn("package com.monikaafterstory.tec.es;", source)
        self.assertIn("UsageStatsManager", source)
        self.assertIn("Settings.ACTION_USAGE_ACCESS_SETTINGS", source)
        self.assertIn('SNAPSHOT_FILE = ".awareness"', source)
        self.assertIn("writeSnapshot", source)
        self.assertIn("scheduleAwarenessNotification", source)
        self.assertIn("NotificationHelper.scheduleExactNotification", source)
        self.assertIn('"mas_awareness_notif"', source)
        self.assertNotIn("NotificationListenerService", source)
        self.assertNotIn("MediaSessionManager", source)

    def test_renpy_activity_lifecycle_hooks_are_registered_without_custom_activity(self):
        source = read_text(RAPT_MANIFEST)
        awareness_source = read_text(RAPT_JAVA)

        self.assertIn('android:name="org.renpy.android.PythonSDLActivity"', source)
        self.assertNotIn("MASActivity", source)
        self.assertIn("ActivityLifecycleCallbacks", awareness_source)
        self.assertIn("registerActivityLifecycleCallbacks", awareness_source)
        self.assertIn("onActivityPaused", awareness_source)
        self.assertIn("onActivityResumed", awareness_source)

    def test_package_usage_stats_permission_is_declared_in_project_and_template(self):
        for path in (RAPT_MANIFEST, RAPT_TEMPLATE_MANIFEST):
            source = read_text(path)
            matches = re.findall(r'android\.permission\.PACKAGE_USAGE_STATS', source)
            self.assertEqual(1, len(matches), str(path))


if __name__ == "__main__":
    unittest.main()
