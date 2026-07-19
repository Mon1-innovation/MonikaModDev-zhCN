init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_test_progressbar",
            category=["dev"],
            prompt="测试进度条",
            pool=True,
            unlocked=True
        )
    )

label dev_test_progressbar:
    "准备显示进度条..."
    $ show_progress_example()
    "处理完成！"
    return