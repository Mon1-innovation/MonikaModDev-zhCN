# Baseline Read Set

- `Monika After Story/game/0_0android_permissions.rpy`: current canonical owner
  of Android permission checks and requests.
- `Monika After Story/game/0mobile.rpy`: consumes the permission result before
  selecting external save and log paths.
- `Monika After Story/game/0utils.rpy`: exposes the observed early external-log
  failure when permission has not completed.
- `tests/test_android_permissions_source.py`: existing Android permission source
  regression tests.
- Git commit `84b730043`: introduced the Ren'Py permission flow.
- Git commit `163f40791`: replaced it with direct Activity permission requests.

## Facts and unknowns

- Fact: the old flow called `renpy.request_permission` from `python early` before
  external storage initialization.
- Fact: the current API `< 30` branch calls Activity `requestPermissions`, which
  returns before the permission callback.
- Fact: the reported API 28 failure occurs while creating
  `/storage/emulated/0/MAS/log` during script loading.
- Unknown: no API 28 device or emulator is attached to this workspace, so the
  actual system permission dialog remains a manual verification item.
