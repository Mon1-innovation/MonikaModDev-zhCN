# Android SDK 28 Permission Compatibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use aegis:subagent-driven-development (recommended) or aegis:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore the historical Ren'Py permission request path on Android API 28 and older while preserving all newer Android permission paths.

**Architecture:** Keep `0_0android_permissions.rpy` as the single permission owner. Add a legacy branch selected from `Build.VERSION.SDK_INT`, and keep `0mobile.rpy` as a consumer of the helper rather than restoring a duplicate permission implementation there.

**Tech Stack:** Ren'Py script Python, PyJNIus, Python `unittest` source regression tests.

---

### Task 1: Lock the compatibility contract in a failing test

**Files:**
- Modify: `tests/test_android_permissions_source.py`

- [x] Require an explicit `sdk_int <= 28` branch.
- [x] Require `renpy.check_permission` and `renpy.request_permission` inside that branch.
- [x] Require the direct Activity request to remain outside the legacy branch.
- [x] Run the target test and confirm it fails for the missing legacy branch.

### Task 2: Restore the legacy request branch

**Files:**
- Modify: `Monika After Story/game/0_0android_permissions.rpy`

- [x] Use Ren'Py permission checks for the API 28-and-older permission status.
- [x] Request legacy storage permissions through `renpy.request_permission`.
- [x] Preserve API 29, API 30+, and API 33+ behavior.
- [x] Keep permission ownership out of `0mobile.rpy`.
- [x] Run the target test and confirm it passes.

### Task 3: Verify related Android behavior

**Files:**
- Verify: `tests/test_android_permissions_source.py`
- Verify: `tests/test_renpy_log_location_source.py`
- Verify: other `tests/test_android_*_source.py` tests

- [x] Run the focused permission tests.
- [x] Run related Android source regressions.
- [x] Inspect the final diff for unrelated changes.
- [x] Record the lack of physical API 28 verification as residual risk.

## Repair and retirement tracks

- Repair: API 28 and older regain the Ren'Py permission adapter that historically
  completed before external storage initialization.
- Retirement: the direct Activity request no longer owns API 28 and older, but
  remains active for API 29. The legacy path can retire when API 28 support is
  intentionally dropped.
