init -850 python:
    import os

    def _mas_persistent_load_error_reasons():
        """
        Builds the Android startup persistent-load warning body from the early
        persistent checker state.
        """
        from store import mas_per_check

        reasons = list()

        if mas_per_check.is_per_incompatible():
            reasons.append(
                "persistent: 存档版本 v{0} 与当前 MAS v{1} 不兼容。".format(
                    mas_per_check.mas_per_version,
                    renpy.config.version
                )
            )

        if mas_per_check.is_per_corrupt():
            reasons.append(
                "persistent: 主存档文件无法解压或反序列化，可能已经损坏。"
            )

        for backup_name in mas_per_check.mas_bad_backups:
            reasons.append(
                "{0}: 该备份也无法读取，已被跳过。".format(backup_name)
            )

        if mas_per_check.mas_backup_copy_failed:
            reasons.append(
                "{0}: 找到了可读取的备份，但无法复制覆盖当前 persistent。".format(
                    mas_per_check.mas_backup_copy_filename or "persistent backup"
                )
            )

        if mas_per_check.mas_no_backups_found:
            reasons.append(
                "persistent*.bak: 没有找到可用的备份存档。"
            )

        if not reasons:
            return None

        early_log_path = os.path.join(renpy.config.basedir, "log", "early.log")
        raw_errors = list()

        for filename, error_detail in mas_per_check.mas_per_raw_errors:
            raw_errors.extend([
                "[{0}]".format(filename),
                error_detail.strip() or "(empty error detail)"
            ])

        if raw_errors:
            raw_error_text = "\n\n".join(raw_errors)
        else:
            raw_error_text = "没有捕获到可直接显示的原始异常；请查看 early.log。"

        return "\n".join([
            "加载失败原因：",
            "\n".join("- " + reason for reason in reasons),
            "",
            "原始报错：",
            raw_error_text,
            "",
            "存档目录：{0}".format(renpy.config.savedir),
            "early.log：{0}".format(early_log_path),
            "",
            "反馈问题时请优先提供 early.log；它记录了启动早期读取 persistent 和备份文件时的完整错误。"
        ])


    def mas_persistent_load_error_dialog():
        if not renpy.android:
            return

        message = _mas_persistent_load_error_reasons()
        if not message:
            return

        try:
            window = AndroidAlertDialog(
                title="你的存档加载出现了问题",
                message=message,
                positive_text="知道了",
                negative_text=""
            )
            window.AsyncTaskerCheck.wait()

        except Exception:
            import traceback
            traceback.print_exc()


    config.start_callbacks.append(mas_persistent_load_error_dialog)
