from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "utils" / "build-android.ps1"
AUTO_SCRIPT = ROOT / "utils" / "build-android-auto.ps1"
AWARENESS_SOURCE = (
    ROOT
    / "docs"
    / "android-notification-java-source"
    / "AwarenessService.java"
)


class AndroidBuildScriptSourceTests(unittest.TestCase):

    def test_notification_source_snapshot_includes_awareness_service(self):
        self.assertTrue(AWARENESS_SOURCE.exists())

        source = AWARENESS_SOURCE.read_text(encoding="utf-8")
        self.assertIn("public class AwarenessService", source)
        self.assertIn("public static String buildState(Context context)", source)

    def test_auto_wrapper_builds_the_current_checkout(self):
        source = AUTO_SCRIPT.read_text(encoding="utf-8-sig")

        self.assertIn("$projectRoot = Split-Path $PSScriptRoot -Parent", source)
        self.assertIn('$buildScript = Join-Path $PSScriptRoot "build-android.ps1"', source)
        self.assertIn('-ProjectBase $projectBase', source)
        self.assertIn('-DDLCBase $ddlcBase', source)
        self.assertNotIn('J:\\MAS\\MonikaModDev-zhCN', source)
        self.assertNotIn("Split-Path (Split-Path $PSScriptRoot -Parent) -Parent", source)

    def test_missing_notification_json_does_not_abort_android_source_sync(self):
        source = SCRIPT.read_text(encoding="utf-8-sig")

        self.assertIn("if (Test-Path $notificationJsonSource)", source)
        self.assertIn("notifications.json not found; skipping optional sync", source)
        self.assertNotIn('Write-Error-Custom "notifications.json missing:', source)

    def test_output_directory_keeps_only_latest_apk(self):
        source = SCRIPT.read_text(encoding="utf-8-sig")

        self.assertIn(
            "$latestApk = $generatedApks | Sort-Object LastWriteTime -Descending | Select-Object -First 1",
            source
        )
        self.assertIn(
            'Get-ChildItem -Path $OutputDir -Filter "*.apk"',
            source
        )
        self.assertIn(
            '$_.FullName -ne $destPath',
            source
        )
        self.assertIn(
            "Remove-Item -Force",
            source
        )
        self.assertIn(
            '$generatedApks | ForEach-Object',
            source
        )
        self.assertIn(
            '已清理 SDK APK: $($_.FullName)',
            source
        )
        self.assertNotIn(
            "# 复制所有 APK 到输出目录",
            source
        )


if __name__ == "__main__":
    unittest.main()
