from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "utils" / "build-android.ps1"


class AndroidBuildScriptSourceTests(unittest.TestCase):

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
