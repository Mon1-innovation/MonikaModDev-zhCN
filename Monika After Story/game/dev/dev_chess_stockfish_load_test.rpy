init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_chess_stockfish_load_test",
            category=["dev"],
            prompt="测试Stockfish引擎加载",
            pool=True,
            unlocked=True
        )
    )

    def mas_dev_chess_stockfish_load_test():
        import os
        import platform
        import subprocess
        import sys

        def _bool_text(value):
            return "是" if value else "否"

        def _path_info(label, path):
            exists = os.path.exists(path)
            lines = [
                "{0}: {1}".format(label, path),
                "  path.exists: {0}".format(exists)
            ]

            if exists:
                try:
                    stat_result = os.stat(path)
                    lines.append("  size: {0}".format(stat_result.st_size))
                    lines.append("  mode: {0:o}".format(stat_result.st_mode))
                    lines.append("  executable: {0}".format(os.access(path, os.X_OK)))
                except Exception as ex:
                    lines.append("  stat failed: {0}".format(ex))

            return lines

        def _android_supported_abis():
            if not renpy.android:
                return "非Android"

            try:
                from jnius import autoclass
                return ", ".join(list(autoclass("android.os.Build").SUPPORTED_ABIS))
            except Exception as ex:
                return "读取失败: {0}".format(ex)

        def _android_sdk_int():
            if not renpy.android:
                return "非Android"

            try:
                from jnius import autoclass
                VERSION = autoclass("android.os.Build$VERSION")
                return str(VERSION.SDK_INT)
            except Exception as ex:
                return "读取失败: {0}".format(ex)

        def _select_engine_path():
            is_64_bit = sys.maxsize > 2**32
            android_binaries = {
                "arm64-v8a": "stockfish-8-arm64-v8a",
                "armeabi-v7a": "stockfish-8-armeabi-v7a",
            }
            android_native_name = "libmas_stockfish.so"

            if renpy.android:
                try:
                    from jnius import autoclass
                    Build = autoclass("android.os.Build")
                    VERSION = autoclass("android.os.Build$VERSION")

                    if VERSION.SDK_INT >= 29:
                        activity = autoclass("org.renpy.android.PythonSDLActivity").mActivity
                        return (
                            os.path.join(
                                activity.getApplicationInfo().nativeLibraryDir,
                                android_native_name
                            ),
                            False
                        )

                    supported_abis = list(Build.SUPPORTED_ABIS)
                except Exception:
                    supported_abis = ("arm64-v8a",) if is_64_bit else ("armeabi-v7a",)

                selected_binary = None
                for abi in supported_abis:
                    if abi in android_binaries:
                        selected_binary = android_binaries[abi]
                        break

                if selected_binary is None:
                    selected_binary = android_binaries["arm64-v8a" if is_64_bit else "armeabi-v7a"]

                return (
                    "/data/user/0/and.sirp.masmobile/files/game/mod_assets/games/chess/{0}".format(selected_binary),
                    True
                )

            if renpy.windows:
                return (
                    os.path.join(
                        renpy.config.gamedir,
                        "mod_assets/games/chess/stockfish_8_windows_x{0}.exe".format("64" if is_64_bit else "32")
                    ),
                    False
                )

            if is_64_bit:
                return (
                    os.path.join(
                        renpy.config.gamedir,
                        "mod_assets/games/chess/stockfish_8_{0}_x64".format("linux" if renpy.linux else "macosx")
                    ),
                    True
                )

            return None, False

        def _run_stockfish(path, should_chmod):
            if not path:
                return ["未选择引擎路径: 当前平台/架构不在既有逻辑支持范围内."]

            if not os.path.exists(path):
                return ["跳过调用测试: 引擎文件不存在."]

            startupinfo = None
            if renpy.windows:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            if should_chmod:
                try:
                    os.chmod(path, 0o755)
                except Exception as ex:
                    return ["chmod 0o755 失败: {0}".format(ex)]

            proc = None
            try:
                proc = subprocess.Popen(
                    path.replace("\\", "/"),
                    bufsize=0,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    startupinfo=startupinfo
                )

                stdout, _stderr = proc.communicate(b"uci\nisready\nquit\n", timeout=5)
                output = stdout.decode("utf-8", errors="replace")
                lines = [
                    "调用测试: 成功启动",
                    "returncode: {0}".format(proc.returncode),
                    "uciok: {0}".format("uciok" in output),
                    "readyok: {0}".format("readyok" in output),
                    "输出:"
                ]
                lines.extend(output.splitlines()[:80])
                return lines

            except subprocess.TimeoutExpired:
                if proc is not None:
                    proc.kill()
                    proc.communicate()
                return ["调用测试超时: Stockfish未在5秒内完成UCI握手."]

            except Exception as ex:
                return ["调用测试失败: {0}: {1}".format(type(ex).__name__, ex)]

        game_chess_dir = os.path.join(renpy.config.gamedir, "mod_assets/games/chess")
        selected_path, should_chmod = _select_engine_path()
        candidate_paths = [
            os.path.join(game_chess_dir, "stockfish_8_windows_x64.exe"),
            os.path.join(game_chess_dir, "stockfish_8_windows_x32.exe"),
            os.path.join(game_chess_dir, "stockfish_8_linux_x64"),
            os.path.join(game_chess_dir, "stockfish_8_macosx_x64"),
            os.path.join(game_chess_dir, "stockfish-8-arm64-v8a"),
            os.path.join(game_chess_dir, "stockfish-8-armeabi-v7a"),
        ]

        if renpy.android:
            try:
                from jnius import autoclass
                activity = autoclass("org.renpy.android.PythonSDLActivity").mActivity
                candidate_paths.append(
                    os.path.join(
                        activity.getApplicationInfo().nativeLibraryDir,
                        "libmas_stockfish.so"
                    )
                )
            except Exception:
                pass

        info = [
            "查看历史以查看全部输出.",
            "",
            "[系统架构]",
            "renpy.windows: {0}".format(_bool_text(renpy.windows)),
            "renpy.linux: {0}".format(_bool_text(renpy.linux)),
            "renpy.macintosh: {0}".format(_bool_text(renpy.macintosh)),
            "renpy.android: {0}".format(_bool_text(renpy.android)),
            "sys.platform: {0}".format(sys.platform),
            "platform.system: {0}".format(platform.system()),
            "platform.machine: {0}".format(platform.machine()),
            "64-bit: {0}".format(_bool_text(sys.maxsize > 2**32)),
            "Android SDK_INT: {0}".format(_android_sdk_int()),
            "Android SUPPORTED_ABIS: {0}".format(_android_supported_abis()),
            "",
            "[目录]",
            "basedir: {0}".format(renpy.config.basedir),
            "gamedir: {0}".format(renpy.config.gamedir),
            "chess assets dir: {0}".format(game_chess_dir),
            "chess assets dir exists: {0}".format(os.path.exists(game_chess_dir)),
            "",
            "[引擎路径]",
            "按当前平台选择: {0}".format(selected_path),
            "调用前chmod: {0}".format(_bool_text(should_chmod)),
        ]

        for candidate_path in candidate_paths:
            info.extend(_path_info(os.path.basename(candidate_path), candidate_path))

        info.extend(["", "[调用测试]"])
        info.extend(_run_stockfish(selected_path, should_chmod))

        return "\n".join(info)


label dev_chess_stockfish_load_test:
    $ result = mas_dev_chess_stockfish_load_test()
    "[result]"
    return
