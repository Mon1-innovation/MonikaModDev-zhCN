init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_demote_aff_version",
            category=["dev"],
            prompt="回退好感度版本",
            pool=True,
            unlocked=True
        )
    )

label dev_demote_aff_version:
    "回退好感度版本将重新读取你的旧版本好感等级, 并覆盖你当前的好感值"
    if not persistent._mas_affection:
        "!!警告: 当前存档没有旧版本好感数据, 执行后将重置你的好感值为0!!!"
    elif persistent._mas_affection.get("affection", 0.0) < 0.1:
        "!!警告: 当前存档没有旧版本好感数据, 执行后将重置你的好感值为0!!!"
    else:
        "好感迁移将以你的旧版好感值[persistent._mas_affection.get('affection', 0.0)]进行计算"
    call p_confirm_calllabel("demote_aff_version")
    return