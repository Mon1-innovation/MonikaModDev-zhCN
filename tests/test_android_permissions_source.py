from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "Monika After Story" / "game"


def read_game_file(name):
    return (GAME_DIR / name).read_text(encoding="utf-8")


class AndroidPermissionSourceTests(unittest.TestCase):

    def test_android_permission_helper_matches_sibling_flow(self):
        source = read_game_file("0_0android_permissions.rpy")

        self.assertIn("def mas_get_current_activity", source)
        self.assertIn("def mas_android_has_permission", source)
        self.assertIn("def mas_android_check_and_request_permissions", source)
        self.assertIn("ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION", source)
        self.assertIn("isExternalStorageManager()", source)
        self.assertIn("current_activity.requestPermissions([", source)
        self.assertIn('"android.permission.WRITE_EXTERNAL_STORAGE"', source)
        self.assertIn('"android.permission.READ_EXTERNAL_STORAGE"', source)
        self.assertIn('"android.permission.POST_NOTIFICATIONS"', source)

    def test_android_manifest_permissions_are_declared_in_options_build_config(self):
        source = read_game_file("options.rpy")

        self.assertIn("build.android_permissions", source)
        self.assertNotIn("config.android_permissions", source)
        self.assertNotIn('hasattr(config, "android_permissions")', source)
        for permission in (
            "android.permission.VIBRATE",
            "android.permission.INTERNET",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.MANAGE_EXTERNAL_STORAGE",
            "android.permission.POST_NOTIFICATIONS",
            "android.permission.SCHEDULE_EXACT_ALARM",
        ):
            self.assertIn(permission, source)

    def test_legacy_init_permission_request_is_retired_from_mobile_bootstrap(self):
        source = read_game_file("0mobile.rpy")

        self.assertNotIn("def req_perm", source)
        self.assertNotIn("renpy.request_permission", source)
        self.assertNotIn("build.android_permissions = p_perms", source)
        self.assertIn("renpy.android and not os.path.exists", source)
        self.assertIn("mas_android_has_permission()", source)

    def test_android_permission_request_is_registered_before_splashscreen(self):
        source = read_game_file("0_0android_permissions.rpy")

        self.assertIn("def mas_android_early_check_and_request_permissions", source)
        self.assertIn("mas_android_early_check_and_request_permissions()", source)
        self.assertIn("def mas_android_startup_permission_check", source)
        self.assertIn("config.start_callbacks.append(mas_android_startup_permission_check)", source)

    def test_splashscreen_no_longer_requests_android_permissions(self):
        source = read_game_file("splash.rpy")
        splash_source = source[source.index("label splashscreen:"):]

        self.assertNotIn("mas_android_has_permission", splash_source)
        self.assertNotIn("mas_android_check_and_request_permissions", splash_source)

    def test_android_farewell_selection_state_is_initialized_before_quit(self):
        source = read_game_file("script-farewells.rpy")

        self.assertIn(
            "default mas_android_selected_farewell_label = None",
            source[:source.index("label mas_farewell_start:")]
        )


if __name__ == "__main__":
    unittest.main()
