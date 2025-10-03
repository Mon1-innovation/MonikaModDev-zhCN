init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_test_confirmwindow",
            category=["dev"],
            prompt="测试确认框",
            pool=True,
            unlocked=True
        )
    )

label dev_test_confirmwindow:
    "准备显示进度条..."
    $ res = show_alert_dialog_example()
    "处理完成！结果为[res]"
    return