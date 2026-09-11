python early:
    _mas_android_classes = None
    _mas_android_permissions_requested = False

    def _mas_android_get_classes():
        global _mas_android_classes

        if not renpy.android:
            return None

        if _mas_android_classes is not None:
            return _mas_android_classes

        try:
            from jnius import autoclass

            classes = {
                "Environment": autoclass("android.os.Environment"),
                "Intent": autoclass("android.content.Intent"),
                "Settings": autoclass("android.provider.Settings"),
                "Uri": autoclass("android.net.Uri"),
                "VERSION": autoclass("android.os.Build$VERSION"),
                "PackageManager": autoclass("android.content.pm.PackageManager"),
                "PythonSDLActivity": None,
                "PythonActivity": None,
            }

            try:
                classes["PythonSDLActivity"] = autoclass("org.renpy.android.PythonSDLActivity")
            except Exception:
                pass

            try:
                classes["PythonActivity"] = autoclass("org.renpy.android.PythonActivity")
            except Exception:
                pass

            _mas_android_classes = classes
            return classes

        except Exception:
            return None

    def mas_get_current_activity():
        if not renpy.android:
            return None

        classes = _mas_android_get_classes()
        if classes is None:
            return None

        activity = None
        python_sdl_activity = classes.get("PythonSDLActivity")
        if python_sdl_activity is not None:
            try:
                activity = python_sdl_activity.mActivity
            except Exception:
                pass

        python_activity = classes.get("PythonActivity")
        if activity is None and python_activity is not None:
            try:
                activity = python_activity.mActivity
            except Exception:
                pass

        return activity

    def mas_android_has_permission():
        if not renpy.android:
            return True

        try:
            classes = _mas_android_get_classes()
            if classes is None:
                return False

            sdk_int = classes["VERSION"].SDK_INT

            if sdk_int <= 28:
                return (
                    renpy.check_permission("android.permission.WRITE_EXTERNAL_STORAGE")
                    and renpy.check_permission("android.permission.READ_EXTERNAL_STORAGE")
                )

            current_activity = mas_get_current_activity()
            if current_activity is None:
                return False

            if sdk_int >= 30:
                return classes["Environment"].isExternalStorageManager()

            result = current_activity.checkSelfPermission(
                "android.permission.WRITE_EXTERNAL_STORAGE"
            )
            return result == classes["PackageManager"].PERMISSION_GRANTED

        except Exception:
            return False

    def mas_android_check_and_request_permissions():
        global _mas_android_permissions_requested

        if not renpy.android:
            return

        try:
            classes = _mas_android_get_classes()
            if classes is None:
                return

            sdk_int = classes["VERSION"].SDK_INT

            # Original target-28 releases used Ren'Py's synchronous SDL bridge.
            if sdk_int <= 28:
                for permission in (
                    "android.permission.WRITE_EXTERNAL_STORAGE",
                    "android.permission.READ_EXTERNAL_STORAGE",
                ):
                    if not renpy.check_permission(permission):
                        renpy.request_permission(permission)

                _mas_android_permissions_requested = True
                return

            current_activity = mas_get_current_activity()
            if current_activity is None:
                return

            if sdk_int >= 30:
                if not classes["Environment"].isExternalStorageManager():
                    try:
                        intent = classes["Intent"](
                            classes["Settings"].ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION
                        )
                        package_uri = classes["Uri"].parse(
                            "package:" + current_activity.getPackageName()
                        )
                        intent.setData(package_uri)
                        current_activity.startActivity(intent)
                    except Exception:
                        pass
            else:
                current_activity.requestPermissions([
                    "android.permission.WRITE_EXTERNAL_STORAGE",
                    "android.permission.READ_EXTERNAL_STORAGE",
                ], 102)

            if sdk_int >= 33:
                current_activity.requestPermissions([
                    "android.permission.POST_NOTIFICATIONS"
                ], 101)

            _mas_android_permissions_requested = True

        except Exception:
            pass

    def mas_android_early_check_and_request_permissions():
        if not renpy.android:
            return

        mas_android_check_and_request_permissions()

    def mas_android_startup_permission_check():
        if not renpy.android:
            return

        if not mas_android_has_permission():
            mas_android_check_and_request_permissions()

            while not mas_android_has_permission():
                renpy.pause(0.1)

            renpy.quit()

        elif not _mas_android_permissions_requested:
            mas_android_check_and_request_permissions()

    mas_android_early_check_and_request_permissions()

init -1590 python:
    if renpy.android:
        config.start_callbacks.append(mas_android_startup_permission_check)
