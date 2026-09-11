init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_android_notifications",
            category=["dev", "维护功能"],
            prompt="Android通知测试",
            pool=True,
            unlocked=True
        )
    )

label dev_android_notifications:
    m "要测试哪一种 Android 通知呢?{nw}"
    menu:
        "要测试哪一种 Android 通知呢?{fast}"
        "立即通知":
            $ _ok = store.mas_android_send_test_notif("[m_name]", "这是一条 Android 立即通知测试。")
            if _ok:
                m "已经请求发送立即通知了。"
            else:
                m "通知请求没有成功。可以检查 Android 权限和 Java 日志。"

        "5秒后定时通知":
            $ _ok = store.mas_android_schedule_notif("[m_name]", "这是一条 Android 定时通知测试。", 5)
            if _ok:
                m "已经请求安排 5 秒后的通知了。"
            else:
                m "定时通知请求没有成功。可以检查 Android 权限和 Java 日志。"

        "清理通知":
            $ store.mas_android_clear_active_notifications()
            m "已经请求清理通知。"

        "取消":
            m "好吧。"

    return
