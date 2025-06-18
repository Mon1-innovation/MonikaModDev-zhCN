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
    call p_confirm_calllabel("demote_aff_version")
    return