# Affection related checks

default persistent._mas_disable_sorry = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_save_check",
            category=["dev"],
            prompt="PERSISTENT CHECK/存档检测",
            pool=True,
            unlocked=True
        )
    )

label dev_save_check:
    python:
        res = store.start_persistent_check(persistent)
        if len(res) > 0:
            renpy.say(m, "You Persistent maybe have a problem/存档保存存在问题, 请查看mas.log")
        else:
            renpy.say(m, "No problems found/无问题")

