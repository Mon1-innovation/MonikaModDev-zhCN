# Android SDK 28 Permission Compatibility

Restore the historical Ren'Py runtime-permission flow for Android devices with
`SDK_INT <= 28` without changing the permission handling used by newer Android
versions.

## Compatibility boundary

- Android API 28 and older: use `renpy.check_permission` and
  `renpy.request_permission` during `python early` initialization.
- Android API 29: retain the existing Activity `requestPermissions` path.
- Android API 30 and newer: retain the all-files-access settings path.
- Android API 33 and newer: retain the notification permission request.

The APK's current `targetSdkVersion` is outside this task. This change branches
on the device's `SDK_INT`.
