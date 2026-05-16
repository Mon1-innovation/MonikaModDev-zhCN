# Android Native Executable Packaging Summary

Date: 2026-05-14

This documents the Android native executable packaging change for MAS Chinese Android builds.

## Background

The old Android executable flow released Stockfish and ImageMagick as data files under:

```text
/data/user/0/and.sirp.masmobile/files/game/mod_assets/games/chess/stockfish-8-*
/data/user/0/and.sirp.masmobile/files/game/magick
```

and then tried to `chmod 755` before launching them with `subprocess.Popen` or
`subprocess.check_output`.

For Android 10/API 29 and newer this is no longer reliable because executing binaries from an app-writable data directory violates Android's W^X policy. `/data/data` and `/data/user/0` are not a meaningful workaround here; for the primary user they point to the same app-private data area.

## New Behavior

Android API 29+ launches native executables from the APK native library directory:

```text
<nativeLibraryDir>/libmas_stockfish.so
<nativeLibraryDir>/libmas_magick.so
```

The APK now contains:

```text
lib/arm64-v8a/libmas_stockfish.so
lib/armeabi-v7a/libmas_stockfish.so
lib/arm64-v8a/libmas_magick.so
lib/arm64-v8a/libomp.so
```

Android API 28 and older keeps the legacy data-file extraction and `chmod` path.

`magick` is currently an arm64-v8a ELF in the repo, so it is only packaged as
`lib/arm64-v8a/libmas_magick.so`.

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

Data package install now releases legacy executable data files only when:

```python
VERSION.SDK_INT < 29
```

This avoids confusing modern Android builds by releasing data-file executables that are no longer the primary execution path.

For ImageMagick:

- API 29+: `ANDROID_MAGICK_BINPATH` points at `nativeLibraryDir/libmas_magick.so` and skips `chmod`.
- API 28 and older: `ANDROID_MAGICK_BINPATH` keeps `/data/user/0/.../files/game/magick` and runs `chmod`.
- `LD_LIBRARY_PATH` includes the selected Magick binary directory first, so native-library launches can find native-directory dependencies such as `libomp.so`.

### `Monika After Story/game/dev/dev_chess_stockfish_load_test.rpy`

The dev Stockfish load test follows the same API split as runtime chess:

- API 29+: select `nativeLibraryDir/libmas_stockfish.so` and skip `chmod`.
- API 28 and older: select the legacy `/data/user/0/.../stockfish-8-*` path and try `chmod`.

The test output also prints `Android SDK_INT`, `Android SUPPORTED_ABIS`, the selected engine path, and whether `chmod` will run before launch.

### `Monika After Story/game/dev/dev_magick_env.rpy`

The dev Magick environment test reports:

- Android SDK version.
- selected `ANDROID_MAGICK_BINPATH`.
- whether `chmod` will run before launch.
- legacy data-file path state.
- modern native-library path state.

### `tests/test_android_permissions_source.py`

Source-level regression coverage checks that:

- Android chess knows about `libmas_stockfish.so`.
- `chess.rpy` uses `nativeLibraryDir`.
- Android SDK version checks use `autoclass("android.os.Build$VERSION")`.
- legacy Stockfish extraction is still retained for API 28 and older.
- the dev Stockfish load test uses the native library path on modern Android.
- Android Magick knows about `libmas_magick.so`.
- `0mobile.rpy` uses `nativeLibraryDir` for modern Android Magick and retains legacy extraction for API 28 and older.
- the dev Magick environment test reports the selected path and whether `chmod` will run.
- RAPT copies MAS Android native executables into `jniLibs`.
- quicksave `StringIO` compatibility remains fixed.

## RAPT SDK Files Changed

These files are outside the repo and live under:

```text
J:\Renpy\renpy-8.2.3-sdk
```

### `rapt/buildlib/rapt/build.py`

Added `copy_mas_android_native_executables(assets_dir)`.

After `split_renpy()`, RAPT places game assets under the returned `assets_dir`. The function copies:

```text
<assets_dir>/game/mod_assets/games/chess/stockfish-8-arm64-v8a
<assets_dir>/game/mod_assets/games/chess/stockfish-8-armeabi-v7a
<assets_dir>/game/magick
<assets_dir>/game/libomp.so
```

into:

```text
project/app/src/main/jniLibs/arm64-v8a/libmas_stockfish.so
project/app/src/main/jniLibs/armeabi-v7a/libmas_stockfish.so
project/app/src/main/jniLibs/arm64-v8a/libmas_magick.so
project/app/src/main/jniLibs/arm64-v8a/libomp.so
```

It is called after `copy_libs()`:

```python
copy_libs()
copy_mas_android_native_executables(assets_dir)
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

This makes Android extract native libraries to a real filesystem path so
`subprocess.Popen` can launch `nativeLibraryDir/libmas_stockfish.so` and
`subprocess.check_output` can launch `nativeLibraryDir/libmas_magick.so`.

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

Build with:

```powershell
& 'J:\MAS\MonikaModDev-zhCN\utils\build-android-auto.ps1'
```

Then inspect the newest APK in:

```text
J:\MAS\dists
```

The APK should include:

```text
lib/arm64-v8a/libmas_stockfish.so
lib/armeabi-v7a/libmas_stockfish.so
lib/arm64-v8a/libmas_magick.so
lib/arm64-v8a/libomp.so
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

If the dev Magick test still points at:

```text
/data/user/0/and.sirp.masmobile/files/game/magick
```

on Android API 29+, confirm `0mobile.rpy` uses `nativeLibraryDir/libmas_magick.so`
and the RAPT SDK `build.py` contains `copy_mas_android_native_executables`.
