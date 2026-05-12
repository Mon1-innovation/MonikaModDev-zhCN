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

    def test_android_filetransfer_runtime_is_retired(self):
        mobile_source = read_game_file("0mobile.rpy")
        chess_source = read_game_file("chess.rpy")

        for retired_symbol in (
            "ANDROID_FTSKIPED",
            "ANDROID_DEFBASEDIR",
            "use_filetransfer",
            "pure_sync",
            "gamesyncTask",
            "gameSyncer",
        ):
            self.assertNotIn(retired_symbol, mobile_source)
            self.assertNotIn(retired_symbol, chess_source)

        self.assertFalse((GAME_DIR / "0_0filetransfer_ren.py").exists())
        self.assertFalse((GAME_DIR / "_ft_test.py").exists())

    def test_android_chess_supports_arm64_and_armeabi_v7a_stockfish(self):
        mobile_source = read_game_file("0mobile.rpy")
        chess_source = read_game_file("chess.rpy")

        for binary_name in (
            "stockfish-8-arm64-v8a",
            "stockfish-8-armeabi-v7a",
        ):
            self.assertIn(binary_name, mobile_source)
            self.assertIn(binary_name, chess_source)

        self.assertIn("ANDROID_STOCKFISH_BINARIES", chess_source)
        self.assertIn("SUPPORTED_ABIS", chess_source)
        self.assertIn("android.os.Build", chess_source)
        self.assertIn("def get_android_stockfish_binary", chess_source)
        self.assertNotIn(
            'fp = "/data/user/0/and.sirp.masmobile/files/game/mod_assets/games/chess/stockfish-8-arm64-v8a"',
            chess_source
        )

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
