# Verification Evidence

## Passed

- `python -m unittest tests.test_android_permissions_source -v`
  - 16 tests passed.
- Three focused tests from `tests.test_renpy_log_location_source`
  - 3 tests passed.
- A Python AST parse of the `python early` block in
  `Monika After Story/game/0_0android_permissions.rpy`
  - syntax OK.
- `git diff --check`
  - no whitespace errors.

## Red-green evidence

- The new SDK 28 request test failed before the implementation with no
  `if sdk_int <= 28` branch.
- The new SDK 28 status-check test was independently run in RED state, then
  passed after restoring the branch.

## Known baseline failures

- `tests.test_renpy_log_location_source.test_bootstrap_prefers_log_subdirectory_for_logdir`
  cannot load the missing tracked path `Monika After Story/renpy/bootstrap.py`.
- The broader awareness source suite has pre-existing missing-file and content
  assertion failures unrelated to this permission change.

## Residual risk

No physical Android API 28 device or emulator is attached, so the actual SDL
permission dialog and post-grant external log creation still require manual
device verification.

## Android build-source verification

- `& .\\utils\\build-android-auto.ps1` now resolves the current checkout,
  synchronizes `AwarenessService.java`, warns about the absent optional
  `notifications.json`, and reaches the Ren'Py Android builder.
- The builder then exits with code `-1` because the local Ren'Py SDK requests
  Android configuration before building. This is an environment prerequisite,
  not a source synchronization failure.
