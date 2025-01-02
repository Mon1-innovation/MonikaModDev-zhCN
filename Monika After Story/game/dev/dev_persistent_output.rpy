init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_persistent_in_output",
            category=["dev"],
            prompt="PERSISTENT IN/OUTPUT/存档导入导出",
            pool=True,
            unlocked=True
        )
    )

label dev_persistent_in_output:
    m "嗯...你要导入还是导出呢?{nw}"
    menu:
        "嗯...你要导入还是导出呢?{fast}"
        "导入":
            $ exist = os.path.exists(os.path.join(ANDROID_MASBASE,"characters", "persistent"))
            if not exist:
                m "你还没有存档哦~, 先把存档放在[os.path.join(ANDROID_MASBASE, 'characters', 'persistent')]吧."
                return
            python:
                renpy.persistent.load(os.path.join(ANDROID_MASBASE,"characters", "persistent"))
                renpy.save_persistent()
                android_toast("导入成功")
                os.remove(os.path.join(ANDROID_MASBASE,"characters", "persistent"))
                renpy.quit()
        "导出":
            python:
                import shutil
                shutil.copyfile(renpy.config.savedir + "/persistent", os.path.join(ANDROID_MASBASE,"characters", "persistent"))
                android_toast("导出成功")
                
        "取消":
            m "好吧."
            return
    
    return
