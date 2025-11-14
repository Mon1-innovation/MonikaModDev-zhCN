init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_persistent_in_output",
            category=["dev", "维护功能"],
            prompt="存档导入导出",
            pool=True,
            unlocked=True
        )
    )

label dev_persistent_in_output:
    m "嗯...你要导入还是导出呢?{nw}"
    menu:
        "嗯...你要导入还是导出呢?{fast}"
        "导入1(实际是与当前存档合并, *风险自负*)":
            $ exist = os.path.exists(os.path.join(ANDROID_MASBASE,"characters", "persistent"))
            if not exist:
                m "你还没有存档哦~, 先把存档放在[os.path.join(ANDROID_MASBASE, 'characters', 'persistent')]吧."
                return
            python:
                #import shutil
                #shutil.copyfile(os.path.join(ANDROID_MASBASE,"characters", "persistent"), renpy.config.savedir + "/persistent")
                newdata = renpy.persistent.load(os.path.join(ANDROID_MASBASE,"characters", "persistent"))
                renpy.persistent.merge(newdata)
                android_toast("导入成功")
                os.remove(os.path.join(ANDROID_MASBASE,"characters", "persistent"))
        "导入2(推荐)":
            if os.path.exists(os.path.join(ANDROID_MASBASE, 'saves', 'persistent')):
                m "重启游戏后 你的存档将自动导入~"
            else:
                m "把存档放在[os.path.join(ANDROID_MASBASE, 'saves', 'persistent')]吧."
                return
        "导出":
            call p_outper
            python:
                import shutil
                persistent.closed_self = True
                renpy.save_persistent()
                shutil.copyfile(renpy.config.savedir + "/persistent", os.path.join(ANDROID_MASBASE,"saves", "persistent_current"))
                persistent.closed_self = False
                android_toast("导出成功")
                
        "取消":
            m "好吧."
            return
    
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_oldver_persistent",
            category=["dev"],
            prompt="将存档导出为旧版本可用存档",
            pool=True,
            unlocked=True
        )
    )

label dev_oldver_persistent:
    "你仍然需要根据说明在PC端安装补丁才能使用存档!"
    call p_confirm_calllabel("generate_old_version_persistent")
    if _return is False:
        return
    python:
        import shutil
        persistent.closed_self = True
        renpy.save_persistent()
        shutil.copyfile(renpy.config.savedir + "/persistent", os.path.join(ANDROID_MASBASE,"saves", "persistent_compatible"))
        android_toast("导出成功")
        renpy.pause(1.0)
        renpy.quit()

    return
