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
        info.append("查看历史以查看全部输出.")
        info.append("ANDROID_MAGICK_BINPATH: {}".format(ANDROID_MAGICK_BINPATH))
        info.append("文件存在: {}".format(os.path.exists(ANDROID_MAGICK_BINPATH)))
        if os.path.exists(ANDROID_MAGICK_BINPATH):
            info.append("文件权限: {:o}".format(os.stat(ANDROID_MAGICK_BINPATH).st_mode))
        info.append("TMPDIR: {}".format(os.environ.get('TMPDIR', '未设置')))
        info.append("MAGICK_HOME: {}".format(os.environ.get('MAGICK_HOME', '未设置')))
        info.append("LD_LIBRARY_PATH: {}".format(os.environ.get('LD_LIBRARY_PATH', '未设置')))

        if os.path.exists(ANDROID_MAGICK_BINPATH):
            try:
                result_exec = subprocess.check_output([ANDROID_MAGICK_BINPATH, '-version'], stderr=subprocess.STDOUT, timeout=5)
                info.append("\n执行结果:\n{}".format(result_exec.decode('utf-8', errors='ignore')))
            except Exception as e:
                info.append("\n执行失败: {}".format(str(e)))

        result = "\n".join(info)
    "[result]"
    return
