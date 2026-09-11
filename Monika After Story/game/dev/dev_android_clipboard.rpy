init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_android_clipboard",
            category=["dev", "维护功能"],
            prompt="Android 剪贴板测试",
            pool=True,
            unlocked=True
        )
    )


label dev_android_clipboard:
    m "要测试 Android 剪贴板的哪项功能呢?{nw}"

    menu:
        "要测试 Android 剪贴板的哪项功能呢?{fast}"
        "复制测试文本":
            $ _dev_android_clipboard = AndroidClipboard()
            $ _dev_android_clipboard_copied = _dev_android_clipboard.copy_to_clipboard("这是 Android 剪贴板测试文本。")
            if _dev_android_clipboard_copied:
                m "我已经将测试文本复制到剪贴板了。"
            else:
                m "复制剪贴板失败了。请查看 Android 日志。"

        "读取当前剪贴板":
            $ _dev_android_clipboard = AndroidClipboard()
            $ _dev_android_clipboard_text = _dev_android_clipboard.get_from_clipboard()
            if _dev_android_clipboard_text:
                m "当前剪贴板内容是：[_dev_android_clipboard_text]"
            else:
                m "剪贴板当前没有文本内容。"

        "取消":
            m "好吧。"

    return
