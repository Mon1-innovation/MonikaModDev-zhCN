# Affection related checks

default persistent._mas_disable_sorry = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_save_check",
            category=["dev"],
            prompt="存档检测",
            pool=True,
            unlocked=True
        )
    )


label dev_save_check:
    m "嗯...是觉着存档有什么问题吧? 要不要我给你看一下?{nw}"
    menu:
        "嗯...是觉着存档有什么问题吧? 要不要我给你看一下?{fast}"
        "帮我看一下吧":
            pass
        "点错啦":
            m "好吧."
            m "要是觉着有问题的话可以随时叫我的喔."
            return
        
    python:
        res = store.start_persistent_check(persistent)
        if len(res) > 0:
            renpy.say(m, "You Persistent maybe have a problem/存档保存存在问题, 请查看mas.log")
        else:
            renpy.say(m, "No problems found/无问题")
    
    return
