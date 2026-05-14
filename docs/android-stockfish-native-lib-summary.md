# Android Stockfish Native Library Packaging Summary

Date: 2026-05-14

This documents the Android chess engine packaging change for MAS Chinese Android builds.

## Background

The old Android chess engine flow released Stockfish as a data file under:

```text
/data/user/0/and.sirp.masmobile/files/game/mod_assets/games/chess/stockfish-8-*
```

and then tried to `chmod 755` before launching it with `subprocess.Popen`.

For Android 10/API 29 and newer this is no longer reliable because executing binaries from an app-writable data directory violates Android's W^X policy. `/data/data` and `/data/user/0` are not a meaningful workaround here; for the primary user they point to the same app-private data area.

## New Behavior

Android API 29+ launches Stockfish from the APK native library directory:

```text
<nativeLibraryDir>/libmas_stockfish.so
```

The APK now contains:

```text
lib/arm64-v8a/libmas_stockfish.so
lib/armeabi-v7a/libmas_stockfish.so
```

Android API 28 and older keeps the legacy data-file extraction and `chmod` path.

## Project Files Changed

### `Monika After Story/game/chess.rpy`

Runtime engine selection now branches by Android SDK version:

- API 29+: use `PythonSDLActivity.mActivity.getApplicationInfo().nativeLibraryDir`.
- API 28 and older: keep `/data/user/0/.../stockfish-8-*` plus `os.chmod(fp, 0o755)`.

The Android SDK version check must use PyJNIus' nested-class form:

```python
VERSION = autoclass("android.os.Build$VERSION")
VERSION.SDK_INT
```

Do not use `autoclass("android.os.Build").VERSION.SDK_INT` for this branch. In testing that form caused the selector to fall through to the legacy data-file path even though the APK native library existed and was executable.

The native executable name is:

```text
libmas_stockfish.so
```

### `Monika After Story/game/0mobile.rpy`

Data package install now releases Stockfish files only when:

```python
VERSION.SDK_INT < 29
```

This avoids confusing modern Android builds by releasing a data-file Stockfish that is no longer the primary execution path.

### `Monika After Story/game/dev/dev_chess_stockfish_load_test.rpy`

The dev Stockfish load test follows the same API split as runtime chess:

- API 29+: select `nativeLibraryDir/libmas_stockfish.so` and skip `chmod`.
- API 28 and older: select the legacy `/data/user/0/.../stockfish-8-*` path and try `chmod`.

The test output also prints `Android SDK_INT`, `Android SUPPORTED_ABIS`, the selected engine path, and whether `chmod` will run before launch.

### `tests/test_android_permissions_source.py`

Source-level regression coverage checks that:

- Android chess knows about `libmas_stockfish.so`.
- `chess.rpy` uses `nativeLibraryDir`.
- Android SDK version checks use `autoclass("android.os.Build$VERSION")`.
- legacy Stockfish extraction is still retained for API 28 and older.
- the dev Stockfish load test uses the native library path on modern Android.
- quicksave `StringIO` compatibility remains fixed.

## RAPT SDK Files Changed

These files are outside the repo and live under:

```text
J:\Renpy\renpy-8.2.3-sdk
```

### `rapt/buildlib/rapt/build.py`

Added `copy_mas_stockfish_native_libs(assets_dir)`.

After `split_renpy()`, RAPT places game assets under the returned `assets_dir`. The Stockfish source path is:

```text
<assets_dir>/game/mod_assets/games/chess/stockfish-8-arm64-v8a
<assets_dir>/game/mod_assets/games/chess/stockfish-8-armeabi-v7a
```

The function copies them into:

```text
project/app/src/main/jniLibs/arm64-v8a/libmas_stockfish.so
project/app/src/main/jniLibs/armeabi-v7a/libmas_stockfish.so
```

It is called after `copy_libs()`:

```python
copy_libs()
copy_mas_stockfish_native_libs(assets_dir)
```

### `rapt/templates/app-build.gradle`

Added:

```gradle
packaging {
    jniLibs {
        useLegacyPackaging = true
    }
}
```

This makes Android extract native libraries to a real filesystem path so `subprocess.Popen` can launch `nativeLibraryDir/libmas_stockfish.so`.

### `rapt/project/app/build.gradle`

The same Gradle block was applied to the currently generated project. The template is the persistent source of truth because RAPT can regenerate `project/app/build.gradle`.

## SDK Root Note

A parallel SDK-local note was written here:

```text
J:\Renpy\renpy-8.2.3-sdk\MAS_STOCKFISH_NATIVE_LIB_MOD_SUMMARY.md
```

If the Ren'Py SDK is replaced or refreshed, reapply the RAPT changes from that note.

## Verification

Run:

```powershell
python -m unittest discover -s tests
```

Expected result:

```text
Ran 15 tests
OK
```

Build with:

```powershell
& 'J:\MAS\MonikaModDev-zhCN\utils\build-android-auto.ps1'
```

Then inspect the newest APK in:

```text
J:\MAS\dists
```

The verified build produced:

```text
J:\MAS\dists\and.sirp.masmobile-0.13.0-1778745895-release.apk
```

and included:

```text
lib/arm64-v8a/libmas_stockfish.so   674192 bytes
lib/armeabi-v7a/libmas_stockfish.so 464712 bytes
```

## Troubleshooting

If the APK contains:

```text
lib/arm64-v8a/libmas_stockfish.so
lib/armeabi-v7a/libmas_stockfish.so
```

and the dev test shows `libmas_stockfish.so` as `100755` and executable, but `[调用测试]` still tries:

```text
/data/user/0/and.sirp.masmobile/files/game/mod_assets/games/chess/stockfish-8-*
```

then packaging is not the failing layer. The runtime selector is falling back to the legacy branch. Confirm `chess.rpy`, `0mobile.rpy`, and `dev_chess_stockfish_load_test.rpy` use:

```python
autoclass("android.os.Build$VERSION")
```

and rebuild the APK so the updated `.rpy` logic is included.
