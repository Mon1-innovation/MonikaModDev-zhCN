from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLIPBOARD_SOURCE = ROOT / "Monika After Story" / "game" / "0_1clipbroad_ren.py"
DEV_DIALOG_SOURCE = ROOT / "Monika After Story" / "game" / "dev" / "dev_android_clipboard.rpy"
API_KEYS_SOURCE = ROOT / "Monika After Story" / "game" / "zz_apikeys.rpy"


class AndroidClipboardSourceTests(unittest.TestCase):

    def test_clipboard_uses_renpy_sdl_bridge_and_returns_safe_values(self):
        source = CLIPBOARD_SOURCE.read_text(encoding="utf-8")

        self.assertIn('autoclass("org.libsdl.app.SDLActivity")', source)
        self.assertIn("clipboardSetText", source)
        self.assertIn("clipboardGetText", source)
        self.assertIn('return "" if text is None else str(text)', source)
        self.assertIn('return False', source)
        self.assertNotIn("android_runnable", source)
        self.assertNotIn("ClipboardManager", source)
        self.assertNotIn("ClipData", source)

    def test_dev_dialog_exercises_copy_and_read_paths(self):
        source = DEV_DIALOG_SOURCE.read_text(encoding="utf-8")

        self.assertIn('eventlabel="dev_android_clipboard"', source)
        self.assertIn('"复制测试文本":', source)
        self.assertIn('"读取当前剪贴板":', source)
        self.assertIn("copy_to_clipboard", source)
        self.assertIn("_dev_android_clipboard_copied", source)
        self.assertIn("get_from_clipboard", source)

    def test_api_key_paste_uses_the_safe_android_clipboard_adapter(self):
        source = API_KEYS_SOURCE.read_text(encoding="utf-8")
        paste_block = source[
            source.index("    def screen_paste(feature):"):
            source.index("    def screen_update_cert():")
        ]

        self.assertIn("AndroidClipboard().get_from_clipboard()", paste_block)
        self.assertNotIn("pygame.scrap", paste_block)
        self.assertNotIn(".decode(", paste_block)


if __name__ == "__main__":
    unittest.main()
