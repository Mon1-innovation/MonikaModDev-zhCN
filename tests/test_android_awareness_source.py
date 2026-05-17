import ast
import re
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "Monika After Story" / "game"
AWARENESS_RPY = GAME_DIR / "zz_android_awareness.rpy"
RAPT_MAIN = Path("J:/Renpy/renpy-8.2.3-sdk/rapt/project/app/src/main")
RAPT_JAVA = RAPT_MAIN / "java" / "com" / "monikaafterstory" / "tec" / "es" / "AwarenessService.java"
RAPT_MANIFEST = RAPT_MAIN / "AndroidManifest.xml"
RAPT_TEMPLATE_MANIFEST = Path("J:/Renpy/renpy-8.2.3-sdk/rapt/templates/app-AndroidManifest.xml")
WINDOWUTILS_RPY = GAME_DIR / "zz_windowutils.rpy"
DEV_ANDROID_AWARENESS_RPY = GAME_DIR / "dev" / "dev_android_awareness_debug.rpy"
ANDROID_WRS_CATEGORIES_RPY = GAME_DIR / "zz_android_windowreact_categories.rpy"


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

    def test_android_wrs_category_script_covers_existing_window_reactions(self):
        source = read_text(ANDROID_WRS_CATEGORIES_RPY)
        mapping_match = re.search(
            r"MAS_ANDROID_WRS_CATEGORIES\s*=\s*(\{.*?\n    \})",
            source,
            re.S
        )
        self.assertIsNotNone(mapping_match)

        mapping = ast.literal_eval(mapping_match.group(1))
        wrs_labels = set()

        for path in GAME_DIR.rglob("*.rpy"):
            if path == ANDROID_WRS_CATEGORIES_RPY:
                continue

            wrs_labels.update(
                re.findall(
                    r'eventlabel\s*=\s*"(mas_wrs_[^"]+)"',
                    read_text(path)
                )
            )

        self.assertEqual(wrs_labels, set(mapping))

        for ev_label, patterns in mapping.items():
            self.assertIsInstance(patterns, list, ev_label)
            self.assertTrue(patterns, ev_label)
            for pattern in patterns:
                re.compile(pattern)

        self.assertIn("if renpy.android:", source)
        self.assertIn("store.mas_update_android_wrs_categories", source)
        self.assertIn("persistent._mas_windowreacts_database", source)
        self.assertIn("store.mas_windowreacts.windowreact_db", source)

    def test_awareness_module_defines_direct_java_bridge_and_reaction_helpers(self):
        source = read_text(AWARENESS_RPY)

        self.assertIn("def mas_awareness_read_state", source)
        self.assertIn("def mas_awareness_get_most_recent_app", source)
        self.assertIn("def mas_awareness_get_app_category", source)
        self.assertIn("def mas_awareness_get_app_reaction", source)
        self.assertIn("def mas_awareness_request_usage_permission", source)
        self.assertIn("def mas_awareness_refresh_state", source)
        self.assertIn("store.mas_awareness_get_app_reaction", source)
        self.assertIn("store.mas_awareness_refresh_state", source)
        self.assertIn("persistent._mas_awareness_enabled", source)
        self.assertIn("persistent._mas_awareness_last_app_mention", source)
        self.assertIn("AwarenessService.buildState(PythonActivity.mActivity)", source)
        self.assertIn("def mas_awareness_get_last_state_debug", source)
        self.assertIn("store.mas_awareness_get_last_state_debug", source)
        self.assertIn("_mas_awareness_last_state_error", source)
        self.assertIn("_mas_awareness_last_state_raw_type", source)
        self.assertIn("_mas_awareness_last_state_raw", source)
        self.assertIn("_mas_awareness_log", source)
        self.assertIn("store.mas_utils.mas_log.info", source)
        self.assertNotIn("            mas_log.info", source)
        self.assertIn("str(value.toString())", source)
        self.assertIn("def _mas_awareness_is_string", source)
        self.assertIn("def _mas_awareness_is_dict", source)
        self.assertIn("def _mas_awareness_is_list", source)
        self.assertIn("def _mas_awareness_get_latest_app", source)
        self.assertIn('app.get("last_used", 0)', source)
        self.assertIn("return _mas_awareness_get_latest_app(apps)", source)
        self.assertIn("if _mas_awareness_is_string(parsed_state):", source)
        self.assertIn("parsed_state = json.loads(parsed_state)", source)
        self.assertIn("if not _mas_awareness_is_dict(parsed_state):", source)
        self.assertNotIn("if not isinstance(parsed_state, dict):", source)
        self.assertNotIn('Java state parsed as " + _mas_awareness_last_state_parsed_type', source)
        self.assertNotIn("def mas_awareness_read_snapshot", source)
        self.assertNotIn("store.mas_awareness_read_snapshot", source)
        self.assertNotIn("store.mas_awareness_force_snapshot", source)
        self.assertNotIn("_MAS_AWARENESS_SNAPSHOT_PATH", source)
        self.assertNotIn("_MAS_AWARENESS_POLL_INTERVAL", source)
        self.assertNotIn("_mas_awareness_last_snapshot", source)
        self.assertNotIn("_mas_awareness_last_read_time", source)
        self.assertNotIn("def mas_awareness_clear_snapshot_cache", source)
        self.assertNotIn("store.mas_awareness_clear_snapshot_cache", source)
        self.assertNotIn("AwarenessService.readSnapshot", source)
        self.assertNotIn("AwarenessService.writeSnapshot", source)

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
        self.assertIn('selected store.mas_awareness_has_permission("usage_stats")', notif_screen)
        self.assertIn("Function(mas_awareness_refresh_state)", notif_screen)
        self.assertNotIn("Function(mas_awareness_force_snapshot)", notif_screen)
        self.assertIn("layout.MAS_TT_ANDROID_AWARENESS", source)
        self.assertIn("layout.MAS_TT_ANDROID_AWARENESS_PERMITS", source)

    def test_dev_android_awareness_debug_topic_reports_runtime_values(self):
        source = read_text(DEV_ANDROID_AWARENESS_RPY)

        self.assertIn('eventlabel="dev_android_awareness_debug"', source)
        self.assertIn('prompt="Android 感知调试"', source)
        self.assertIn("screen dev_android_awareness_debug_screen():", source)
        self.assertIn("timer 1.0 action Function(dev_android_awareness_refresh_debug_values) repeat True", source)
        self.assertIn("call screen dev_android_awareness_debug_screen", source)
        self.assertIn("for _dev_android_debug_label, _dev_android_debug_value in store.dev_android_awareness_debug_values:", source)
        self.assertIn("text _dev_android_debug_label", source)
        self.assertIn("text _dev_android_debug_value", source)
        self.assertNotIn("min_width 320", source)
        self.assertIn("def dev_android_awareness_collect_debug_values", source)
        self.assertIn("def dev_android_awareness_refresh_debug_values", source)
        self.assertIn("mas_getActiveWindowHandle()", source)
        self.assertIn("mas_isFocused()", source)
        self.assertIn("store.mas_awareness_read_state()", source)
        self.assertIn('_dev_android_state.get("permissions", {})', source)
        self.assertIn('_dev_android_permissions.get("usage_stats", False)', source)
        self.assertIn("store._mas_awareness_is_dict(_dev_android_state)", source)
        self.assertIn("store._mas_awareness_is_list(_dev_android_apps)", source)
        self.assertIn("store._mas_awareness_get_latest_app(_dev_android_apps)", source)
        self.assertNotIn("_dev_android_apps[-1]", source)
        self.assertNotIn("isinstance(_dev_android_state, dict)", source)
        self.assertNotIn("store.mas_awareness_has_permission", source)
        self.assertNotIn("store.mas_awareness_get_most_recent_app()", source)
        self.assertNotIn("_mas_dev_android_debug_call(mas_isFocused", source)
        self.assertIn("store.mas_awareness_get_last_state_debug()", source)
        self.assertNotIn("store.mas_awareness_read_snapshot()", source)
        self.assertNotIn("store.mas_awareness_force_snapshot()", source)
        self.assertNotIn("store.mas_awareness_clear_snapshot_cache()", source)
        self.assertIn('state.get("mas_activity", {})', source)
        self.assertIn("State keys", source)
        self.assertIn("State bridge error", source)
        self.assertIn("State parsed type", source)
        self.assertIn("State raw type", source)
        self.assertIn("完整 raw state 已写入 mas_log", source)
        self.assertNotIn("State raw preview", source)
        self.assertNotIn("Snapshot keys", source)
        self.assertIn("dev_android_awareness_push_random_wrs", source)
        self.assertIn("store.mas_windowreacts.windowreact_db", source)
        self.assertIn("MASEventList.queue(_dev_android_wrs_label)", source)
        self.assertNotIn("MASEventList.push(_dev_android_wrs_label)", source)
        self.assertIn("_dev_android_wrs_event.unlocked = False", source)
        self.assertIn('replace("{", "{{")', source)
        self.assertIn('replace("}", "}}")', source)

    def test_awareness_java_source_uses_usage_stats_and_existing_notification_helper(self):
        source = read_text(RAPT_JAVA)

        self.assertIn("package com.monikaafterstory.tec.es;", source)
        self.assertIn("UsageStatsManager", source)
        self.assertIn("Settings.ACTION_USAGE_ACCESS_SETTINGS", source)
        self.assertIn("buildState", source)
        self.assertIn("appTimestamps.remove(packageName);", source)
        self.assertIn("appTimestamps.put(packageName, event.getTimeStamp());", source)
        self.assertNotIn("buildSnapshot", source)
        self.assertNotIn('SNAPSHOT_FILE = ".awareness"', source)
        self.assertNotIn("writeSnapshot", source)
        self.assertNotIn("readSnapshot", source)
        self.assertNotIn("new BufferedWriter", source)
        self.assertIn("scheduleAwarenessNotification", source)
        self.assertIn("NotificationHelper.scheduleExactNotification", source)
        self.assertIn('"mas_awareness_notif"', source)
        self.assertNotIn("NotificationListenerService", source)
        self.assertNotIn("MediaSessionManager", source)

    def test_windowutils_enables_android_notifications_and_windowreacts(self):
        source = read_text(WINDOWUTILS_RPY)

        self.assertIn("elif renpy.android:", source)
        self.assertIn("store.mas_windowreacts.can_show_notifs = True", source)
        self.assertIn("store.mas_windowreacts.can_do_windowreacts = True", source)

    def test_windowutils_uses_android_awareness_app_for_active_window(self):
        source = read_text(WINDOWUTILS_RPY)
        android_window_getter = source[
            source.index("def _getActiveWindowHandle_Android() -> str:"):
            source.index("def _isFocused_Android():")
        ]

        self.assertIn("def _getActiveWindowHandle_Android() -> str:", source)
        self.assertIn("store.persistent._mas_awareness_enabled", android_window_getter)
        self.assertNotIn("not persistent._mas_awareness_enabled", android_window_getter)
        self.assertIn('hasattr(store, "mas_awareness_get_most_recent_app")', source)
        self.assertIn("store.mas_awareness_get_most_recent_app()", source)
        self.assertIn("if not store._mas_awareness_is_dict(app):", android_window_getter)
        self.assertIn('return "{} {}".format(app_label, package_name).strip()', source)
        self.assertIn("_window_get = _getActiveWindowHandle_Android", source)

    def test_windowutils_uses_android_activity_state_for_focus(self):
        source = read_text(WINDOWUTILS_RPY)

        self.assertIn("def _isFocused_Android():", source)
        self.assertIn('hasattr(store, "mas_awareness_read_state")', source)
        self.assertIn('state.get("mas_activity", {})', source)
        self.assertIn("if not store._mas_awareness_is_dict(state):", source)
        self.assertIn("if not store._mas_awareness_is_dict(activity):", source)
        self.assertNotIn('hasattr(store, "mas_awareness_read_snapshot")', source)
        self.assertIn('activity.get("resumed", False)', source)
        self.assertIn('activity.get("has_window_focus", False)', source)
        self.assertIn("if renpy.android:", source)
        self.assertIn("return store.mas_windowutils._isFocused_Android()", source)

    def test_android_notifications_respect_group_and_focus_checks(self):
        source = read_text(WINDOWUTILS_RPY)
        display_notif_source = source[source.index("def mas_display_notif("):source.index("    def mas_isFocused():")]

        self.assertIn("if renpy.android and hasattr(store, \"mas_android_display_notif\"):", display_notif_source)
        self.assertIn("skip_checks", display_notif_source)
        self.assertIn("mas_notifsEnabledForGroup(group)", display_notif_source)
        self.assertIn("not mas_isFocused()", display_notif_source)
        self.assertIn("return store.mas_android_display_notif(title, notif_body)", display_notif_source)

    def test_awareness_java_state_includes_mas_activity_state(self):
        source = read_text(RAPT_JAVA)

        self.assertIn('"mas_activity"', source)
        self.assertIn('"resumed"', source)
        self.assertIn('"paused"', source)
        self.assertIn('"stopped"', source)
        self.assertIn('"has_window_focus"', source)
        self.assertIn('"in_picture_in_picture"', source)
        self.assertIn('"in_multi_window"', source)
        self.assertIn("hasWindowFocus()", source)
        self.assertIn("isInPictureInPictureMode()", source)
        self.assertIn("isInMultiWindowMode()", source)

    def test_renpy_activity_lifecycle_hooks_are_registered_without_custom_activity(self):
        source = read_text(RAPT_MANIFEST)
        awareness_source = read_text(RAPT_JAVA)

        self.assertIn('android:name="org.renpy.android.PythonSDLActivity"', source)
        self.assertNotIn("MASActivity", source)
        self.assertIn("ActivityLifecycleCallbacks", awareness_source)
        self.assertIn("registerActivityLifecycleCallbacks", awareness_source)
        self.assertIn("onActivityPaused", awareness_source)
        self.assertIn("onActivityResumed", awareness_source)

    def test_android_awareness_permissions_are_declared_in_project_and_template(self):
        for path in (RAPT_MANIFEST, RAPT_TEMPLATE_MANIFEST):
            source = read_text(path)
            usage_matches = re.findall(r'android\.permission\.PACKAGE_USAGE_STATS', source)
            query_matches = re.findall(r'android\.permission\.QUERY_ALL_PACKAGES', source)
            self.assertEqual(1, len(usage_matches), str(path))
            self.assertEqual(1, len(query_matches), str(path))


if __name__ == "__main__":
    unittest.main()
