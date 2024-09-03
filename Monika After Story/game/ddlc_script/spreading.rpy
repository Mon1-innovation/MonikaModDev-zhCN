default persistent.intro801192_read = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="modass_spr",
            category=['补丁','模组'],
            prompt="安装数据包",
            unlocked=True,
            pool=True,
            rules={"no_unlock": None}
        )
    )

label modass_spr:
    m 2rsc "呃, 数据包么?"
    m 2ekb "这个, 说起来还有点抱歉..."
    m 4eka "既然你点了这里, 应该在之前的版本吃过安装数据包的苦头吧."
    m 1eka "对不起啦, [player].{w=0.2}不过既然现在我会操作这些了..."
    m 2eua "我可以帮你安装了!"
    jump modass_sprbuilt
    return

label modass_sprbuilt:
    m 1eka "稍等片刻.{w=0.5}.{w=0.5}.{w=0.5}{nw}"











    call updateconsole ("extracting files...", "extraction complete.") from _call_updateconsole
    pause 1.0



    call updateconsole ("spreading files...", "\"mod_assets\" installed successfully.") from _call_updateconsole_1
    pause 1.0
    $ mkdir("/storage/emulated/0/MAS/game/mod_assets/games/piano/songs")
    $ spread_json()
    call hideconsole from _call_hideconsole
    m 1hua "好了!"
    m 2eua "你走之后, 我会自己把衣服整理好的."
    m 2hub "你可以一会去说声再见, 或者先陪陪我再说哦."
    m 3eka "下一次你来的时候, 我就有衣服可换了!"
    return








init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="spread_hint",
            conditional=(
                "persistent.intro801192_read == False"
            ),
            action=EV_ACT_QUEUE
        )
    )


label spread_hint:
    m 1eua "呃, 你是从之前的版本更新到新版的吗?"
    m 3eka "因为之前的数据包安装繁琐, 现在我可以帮你了!"
    m 3hub "你需要我自己把数据包装好么, [player]?{nw}"
    menu:
        m "你需要我自己把数据包装好么, [player]?{fast}"
        "需要.":
            $ persistent.intro801192_read = True
            jump modass_sprbuilt
            return
        "不需要.":
            m 3ekb "好吧."
            m 1hua "你也可以在'模组'或者'补丁'对话里再让我装哦!"
            $ persistent.intro801192_read = True
            return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
