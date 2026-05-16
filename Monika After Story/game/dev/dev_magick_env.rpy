init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_test_magick_env",
            category=["dev"],
            prompt="测试ImageMagick环境",
            pool=True,
            unlocked=True
        )
    )

label dev_test_magick_env:
    python:
        import os
        import subprocess
        info = []

        legacy_magick_path = os.path.join(ANDROID_APP_GAME_DIR, ANDROID_LEGACY_MAGICK_NAME)
        native_magick_path = None
        android_sdk_int = "非Android"

        if renpy.android:
            try:
                from jnius import autoclass
                VERSION = autoclass("android.os.Build$VERSION")
                android_sdk_int = str(VERSION.SDK_INT)
                activity = autoclass("org.renpy.android.PythonSDLActivity").mActivity
                native_magick_path = os.path.join(
                    activity.getApplicationInfo().nativeLibraryDir,
                    ANDROID_NATIVE_MAGICK_NAME
                )
            except Exception as e:
                android_sdk_int = "读取失败: {}".format(e)

        info.append("查看历史以查看全部输出.")
        info.append("Android SDK_INT: {}".format(android_sdk_int))
        info.append("ANDROID_MAGICK_BINPATH: {}".format(ANDROID_MAGICK_BINPATH))
        info.append("ANDROID_MAGICK_SHOULD_CHMOD: {}".format(ANDROID_MAGICK_SHOULD_CHMOD))
        info.append("调用前chmod: {}".format("是" if ANDROID_MAGICK_SHOULD_CHMOD else "否"))
        info.append("文件存在: {}".format(os.path.exists(ANDROID_MAGICK_BINPATH)))
        if os.path.exists(ANDROID_MAGICK_BINPATH):
            info.append("文件权限: {:o}".format(os.stat(ANDROID_MAGICK_BINPATH).st_mode))
        info.append("legacy magick: {}".format(legacy_magick_path))
        info.append("legacy存在: {}".format(os.path.exists(legacy_magick_path)))
        if native_magick_path:
            info.append("native libmas_magick.so: {}".format(native_magick_path))
            info.append("native存在: {}".format(os.path.exists(native_magick_path)))
        info.append("TMPDIR: {}".format(os.environ.get('TMPDIR', '未设置')))
        info.append("MAGICK_HOME: {}".format(os.environ.get('MAGICK_HOME', '未设置')))
        info.append("LD_LIBRARY_PATH: {}".format(os.environ.get('LD_LIBRARY_PATH', '未设置')))

        if os.path.exists(ANDROID_MAGICK_BINPATH):
            try:
                if ANDROID_MAGICK_SHOULD_CHMOD:
                    os.chmod(ANDROID_MAGICK_BINPATH, 0o755)
                result_exec = subprocess.check_output([ANDROID_MAGICK_BINPATH, '-version'], stderr=subprocess.STDOUT, timeout=5)
                info.append("\n执行结果:\n{}".format(result_exec.decode('utf-8', errors='ignore')))
            except Exception as e:
                info.append("\n执行失败: {}".format(str(e)))

        result = "\n".join(info)
    "[result]"
    return
