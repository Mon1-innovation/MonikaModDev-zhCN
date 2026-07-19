init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_test_image_selector",
            category=["dev"],
            prompt="测试图片选择器",
            pool=True,
            unlocked=True
        )
    )

label dev_test_image_selector:
    "准备打开图片选择器..."
    $ image_path = select_image()
    menu:
        "你选完了吗？":
            pass
    "选择的图片路径: [image_path.image_path]"
    "是否在选择中：[image_path.is_selecting]"
    return
