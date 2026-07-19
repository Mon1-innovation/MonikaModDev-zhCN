from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DIALOG_SOURCE = (
    ROOT
    / "Monika After Story"
    / "game"
    / "0_persistent_load_error_dialog.rpy"
)
BACKUP_SOURCE = ROOT / "Monika After Story" / "game" / "zz_backup.rpy"


class PersistentLoadErrorDialogSourceTests(unittest.TestCase):

    def test_standalone_file_registers_android_start_callback(self):
        source = DIALOG_SOURCE.read_text(encoding="utf-8")

        self.assertIn("config.start_callbacks.append(mas_persistent_load_error_dialog)", source)
        self.assertIn("if not renpy.android:", source)
        self.assertIn("AndroidAlertDialog(", source)
        self.assertNotIn("label splashscreen:", source)

    def test_dialog_explains_save_load_failure_and_early_log_priority(self):
        source = DIALOG_SOURCE.read_text(encoding="utf-8")

        self.assertIn("你的存档加载出现了问题", source)
        self.assertIn("反馈问题时请优先提供 early.log", source)
        self.assertIn('os.path.join(renpy.config.basedir, "log", "early.log")', source)
        self.assertIn("renpy.config.savedir", source)

    def test_dialog_reports_each_failed_persistent_file_reason(self):
        source = DIALOG_SOURCE.read_text(encoding="utf-8")

        self.assertIn("mas_per_check.mas_bad_backups", source)
        self.assertIn("mas_per_check.mas_backup_copy_filename", source)
        self.assertIn("mas_per_check.mas_backup_copy_failed", source)
        self.assertIn("mas_per_check.mas_no_backups_found", source)
        self.assertIn("mas_per_check.is_per_incompatible()", source)
        self.assertIn("mas_per_check.mas_per_version", source)

    def test_dialog_includes_raw_persistent_load_errors(self):
        source = DIALOG_SOURCE.read_text(encoding="utf-8")

        self.assertIn("原始报错：", source)
        self.assertIn("mas_per_check.mas_per_raw_errors", source)
        self.assertIn("error_detail", source)

    def test_backup_checker_keeps_raw_error_text_for_dialog(self):
        source = BACKUP_SOURCE.read_text(encoding="utf-8")

        self.assertIn("mas_per_raw_errors = list()", source)
        self.assertIn("def _record_per_raw_error", source)
        self.assertIn("traceback.format_exc()", source)
        self.assertIn("mas_per_raw_errors.append", source)
        self.assertIn("_record_per_raw_error(", source)


if __name__ == "__main__":
    unittest.main()
