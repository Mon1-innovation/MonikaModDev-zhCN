python early:    
    import os

    ANDROID_MASBASE = "/storage/emulated/0/MAS/"
    ANDROID_SAVEDIR_CHANGED = False
    ANDROID_APP_GAME_DIR = "/data/user/0/and.sirp.masmobile/files/game"
    ANDROID_MAGICK_BINPATH = os.path.join(ANDROID_APP_GAME_DIR, "magick")
    ANDROID_STOCKFISH_FILES = (
        "mod_assets/games/chess/stockfish-8-arm64-v8a",
        "mod_assets/games/chess/stockfish-8-armeabi-v7a",
    )

    if renpy.android and os.path.exists(ANDROID_MAGICK_BINPATH):
        os.chmod(ANDROID_MAGICK_BINPATH, 0o755)
        os.environ['TMPDIR'] = os.path.join("/data/user/0/and.sirp.masmobile/files/game", "tmp")
        os.environ['MAGICK_HOME'] = os.path.join("/data/user/0/and.sirp.masmobile/files/game")
        os.environ['LD_LIBRARY_PATH'] = os.path.join("/data/user/0/and.sirp.masmobile/files/game")

    #config.savedir = os.path.join(ANDROID_MASBASE, "saves")

    def android_toast(message):
        print("android_toast：", message)
        if not renpy.android:
            return
        from jnius import autoclass, cast
        PYActivity = autoclass("org.renpy.android.PythonSDLActivity")
        PYActivity.toastError(message)
    if renpy.android:
        p_debug = os.path.exists("/storage/emulated/0/MAS/debug.p")
    else:
        p_debug = True
    # debug
    renpy.config.developer = p_debug
    renpy.config.debug = p_debug
    renpy.config.console = p_debug
    renpy.config.save_on_mobile_background = False
    # Kept for compatibility with older debug code that inspected request state.
    p_perm_dict = {}

    def p_raise():
        raise Exception("Raise Exception for Debugging")

    if renpy.android:
        renpy.config.basedir = ANDROID_MASBASE
        renpy.config.gamedir = os.path.join(renpy.config.basedir, "game")
    
    if renpy.android and not os.path.exists("/storage/emulated/0/MAS/use_android_savedir") and mas_android_has_permission():
        renpy.config.savedir = os.path.join(ANDROID_MASBASE, "saves")
        ANDROID_SAVEDIR_CHANGED = True


    #def scan_outer_resource(add, seen):
    #    files = game_files
    #    if renpy.android:
    #        outer = "/storage/emulated/0/MAS/"
    #    else:
    #        return
    #    print("Outer\\", outer, "\\Scaned:")
    #    for each in walkdir(outer):
    #        add(outer, each, files, seen)
    #        print("    ", outer, " - ", each)
    #renpy.loader.scandirfiles_callbacks.append(scan_outer_resource)

    def _error_copyer():
        # 目标目录（游戏根目录下的error_logs文件夹）
        dest_dir = os.path.join(ANDROID_MASBASE, "log")

        try:
            # 确保目标目录存在
            os.makedirs(dest_dir, exist_ok=True)
            
            # 获取当前时间戳
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            
            # 要复制的文件列表
            log_files = [
                ("error.txt", f"error-{timestamp}.txt"),
                ("log.txt", f"log-{timestamp}.txt"),
                ("traceback.txt", f"traceback-{timestamp}.txt")
            ]
            
            # 复制文件
            for src_name, dest_name in log_files:
                src_path = os.path.join(config.logdir, src_name)
                dest_path = os.path.join(dest_dir,  src_name)
                
                if os.path.exists(src_path):
                    shutil.copy2(src_path, dest_path)

        except Exception as e:
            print(f"日志保存失败: {str(e)}")
    
    original_report_exception = renpy.renpy.error.report_exception
    def new_report_exception(*args, **kwargs):
        res = original_report_exception(*args, **kwargs)
        if renpy.android:
            _error_copyer()
            android_toast("x_x 游戏崩溃了, 请查看log文件夹以获取详细信息")

        if renpy.is_init_phase() and renpy.android:
            import time
            window = AndroidAlertDialog(
                title="抱歉, 但是游戏发生了异常...",
                message=res[0]+"\n将在10秒后自动退出...",
                positive_text="",
                negative_text="关闭",
            )
            window.AsyncTaskerCheck.wait()
        return res
    renpy.renpy.error.report_exception = new_report_exception

    # 检查是否试图安装PC版本
    import os
    paths = [
        os.path.join(ANDROID_MASBASE, "game", "zz_windowutils.rpyc"),
        os.path.join(ANDROID_MASBASE, "python-packages", "pywintypes27.dll"),
        os.path.join(ANDROID_MASBASE, "python-packages", "pythoncomloader27.dll"),
        os.path.join(ANDROID_MASBASE, "python-packages", "pythoncom27.dll")
    ]
    for path in paths:
        if os.path.exists(path):
            window = AndroidAlertDialog(
                title="抱歉, 但是你似乎尝试在手机版中安装PC版本...",
                message="手机端和PC端是完全独立的两个版本.\n因为手机端使用更新的Renpy引擎, 所以不支持PC端的代码.\nPC版本也未对手机做任何兼容, 所以你无法打开游戏.\n\n请删除 MAS/game 文件夹后再启动游戏.",
                positive_text="",
                negative_text="关闭",
            )
            window.AsyncTaskerCheck.wait()
            renpy.quit()
    
init 999 python:
    @store.mas_submod_utils.functionplugin("ch30_preloop", priority=-10000)
    def hide_dev():
        if not p_debug:
            if persistent.event_database:
                for evlabel in persistent.event_database:
                    ev = mas_getEV(evlabel)
                    if ev:
                        if ev.category:
                            for c in ev.category:
                                if "dev" in c:
                                    mas_lockEvent(ev)

init python:
    cn_debuging = p_debug
    import os
    def _restart_mas():
        renpy.full_restart()
        renpy.reload_script()
        android_toast("已软重启游戏, 如果回到主菜单是正常现象")
    def mkdir(path):
        if not os.path.exists(path):
            os.makedirs(path)
    def extract_file(file):
        # 解压文件, 仅限于game目录下的文件
        if not renpy.loadable(file):
            store.mas_utils.mas_log.error(f"extract_file: 无法释放文件，因为无法加载'{file}'")
            return []
        
        # 定义目标路径
        target_path = [
            os.path.join("/storage/emulated/0/MAS/game", file),
            os.path.join(ANDROID_APP_GAME_DIR, file),
            ]
        for t in target_path:
            target_dir = os.path.dirname(t)

            # 创建目标目录（如果不存在）
            os.makedirs(target_dir, exist_ok=True)

            # 写入文件
            with open(t, "wb") as f:
                f.write(renpy.loader.load_from_apk(file).read())

        return target_path

    def chmod_executable(path):
        if path.startswith(ANDROID_APP_GAME_DIR):
            try:
                os.chmod(path, 0o755)
            except Exception as e:
                store.mas_utils.mas_log.error(f"chmod_executable: 无法赋予'{path}'可执行权限: {e}")

    def android_uses_legacy_stockfish_files():
        if not renpy.android:
            return False

        try:
            from jnius import autoclass
            VERSION = autoclass("android.os.Build$VERSION")
            return VERSION.SDK_INT < 29

        except Exception:
            return True

    def firstrun_spread():
        spread_json()
        android_toast("数据文件已安装, 推荐重启游戏再游玩")

    def spread_json():
        extract_file("mod_assets/monika/cg/o31rcg")
        extract_file("mod_assets/monika/cg/o31mcg")
        extract_file("mod_assets/monika/cg/o31mcg") 
        extract_file("mod_assets/location/special/our_reality")   
        extract_file("mod_assets/monika/mbase")   
        extract_file("mod_assets/monika/NjM2ODZmNjM2ZjZjNjE3NDY1NzM=")
        extract_file("mod_assets/games/piano/songs/happybirthday.json")
        extract_file("mod_assets/games/piano/songs/yourreality.json")
        if android_uses_legacy_stockfish_files():
            for stockfish_file in ANDROID_STOCKFISH_FILES:
                for target_path in extract_file(stockfish_file):
                    chmod_executable(target_path)
        extract_file("python-packages/certifi/cacert.pem")
        extract_file("magick")
        extract_file("libc++_shared.so")
        extract_file("libomp.so")
        extract_file("audio.rpa")
        extract_file(".nomedia")


    def spread_readme():
        open("/storage/emulated/0/MAS/characters/Readme.txt", "wb").write(renpy.file("Readme.txt").read())

    import os
    default_per = "D:\MAS\MAS-PE-Remake\game\saves\persistent"
    import_per = "D:\MAS\MAS-PE-Remake\game\saves\persistent.bak"
    


    
    

    def start_persistent_check(per:renpy.persistent.Persistent):
        problems = []
        def test_save(per):
            from renpy.compat.pickle import dump, dumps, loads
            return len(dumps(per))


        per2 = renpy.persistent.Persistent()
        for k, v in per.__dict__.items():
            try:
                per2.__dict__[k] = v
                size = test_save(per2)
                store.mas_utils.mas_log.info(f"Persistent check : {k} succeeded, {size} byte")
            except Exception as e:
                store.mas_utils.mas_log.error(f"Persistent check : {k} failed, {e}")
                if k in per2.__dict__:
                    del per2.__dict__[k]
                    problems.append(k)
        
        if len(problems) > 0:
            store.mas_utils.mas_log.error(f"Persistent check found errors on keys : {problems}")
            renpy.notify("Persistent Error Key List:\n {}".format(problems))
        else:
            renpy.notify("Persistent Check Successful")
        return problems
         
label p_outper:
    if ANDROID_SAVEDIR_CHANGED:
        "存档文件夹已被修改, 直接使用 MAS/saves 下的文件即可"
        return
    "即将导出存档"
    python:
        import shutil
        import os

        source_folder = renpy.config.savedir
        destination_folder = os.path.join(ANDROID_MASBASE, 'saves')

        # 如果目标文件夹不存在，则创建
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for filename in os.listdir(source_folder):
            if filename.endswith('.bak'):
                shutil.copy2(os.path.join(source_folder, filename), destination_folder)

    
    "存档已导出至[destination_folder]"
    "如需要重新导入, 请将persistent放置至[destination_folder]下并重启游戏"
    return
label p_confirm_calllabel(alabel):
    menu:
        "你确定要执行操作 [alabel] 吗?"
        "是":
            $ _return = True
            $ renpy.call(alabel)
        "否":
            $ _return = False
    return _return
label generate_old_version_persistent:
    python:
        del persistent._voice_mute
        del persistent._mas_acs_pre_list
        del persistent._mas_windowreacts_notif_filters
        persistent.closed_self = True
        renpy.save_persistent()
    return
label demote_aff_version:
    python:
        persistent._mas_affection_version = 1
        persistent.closed_self = True
        renpy.save_persistent()
        _restart_mas()
    return
label hide_all_dev:
    python:
        for evlabel in persistent.event_database:
            ev = mas_getEV(evlabel)
            if ev:
                if ev.category:
                    for c in ev.category:
                        if "dev" in c:
                            mas_lockEvent(ev)
    return

label show_all_dev:
    python:
        for evlabel in persistent.event_database:
            ev = mas_getEV(evlabel)
            if ev:
                if ev.category:
                    for c in ev.category:
                        if "dev" in c:
                            mas_unlockEvent(ev)
    return

label install_submods:
    python:
        import time
        zip_files = installer.get_zip_files()
        zip_uninstall_files = uninstaller.get_zip_files()

        renpy.say(m, f"一共有{len(zip_files)}个压缩包待安装, {len(zip_uninstall_files)}个压缩包待卸载.")

    python:
        for zip_file in zip_files:
            installtask = AsyncTask(installer.process_zip, zip_file)
            progress = installer.get_progress()
            installprogress = AndroidProgressDialog(
                title="处理中", 
                message="正在加载数据...",
                max_value=100
            )
            while not installtask.is_finished:
                progress = installer.get_progress()
                installprogress.update(
                    progress['progress_percent'],
                    title = f"{progress['stage']}:{progress['current_zip']}",
                    message = f"{progress['processed_files']}/{progress['total_files']}: {progress['current_file']}"
                )
                time.sleep(0.1)
            installprogress.dismiss()
    python:
        for zip_file in zip_uninstall_files:
            uninstaltask = AsyncTask(uninstaller.process_zip, zip_file)
            progress = uninstaller.get_progress()
            uninstallprogress = AndroidProgressDialog(
                title="处理中", 
                message="正在加载数据...",
                max_value=100
            )
            while not uninstaltask.is_finished:
                progress = uninstaller.get_progress()
                uninstallprogress.update(
                    progress['progress_percent'],
                    title = f"{progress['stage']}:{progress['current_zip']}",
                    message = f"{progress['processed_files']}/{progress['total_files']}: {progress['current_file']}"
                )
                time.sleep(0.1)
            uninstallprogress.dismiss()
    return
label create_hint_file:
    $ target_file = ""
    python:
        import os
        def create_hint_file(target_file):
            hint_file = os.path.join(ANDROID_MASBASE, target_file)
            if not os.path.exists(hint_file):
                with open(hint_file, "w") as f:
                    pass
        def delete_hint_file(target_file):
            hint_file = os.path.join(ANDROID_MASBASE, target_file)
            if os.path.exists(hint_file):
                os.remove(hint_file)
        hint_files = [
            {"name": "debug.p", "description": "该文件可以开启开发者模式"},
            {"name": "use_android_savedir", "description": "该文件可以将存档文件夹修改为Android数据文件夹下的默认位置"},
            {"name": "算了", "description": "好吧~"}
        ]
        # 构建菜单项
        menu_items = []
        for f in hint_files:
            menu_items.append((f['name'], f['name']))
        
        # 显示菜单
        choice = renpy.display_menu(menu_items)
                
        target_file = choice
        
        # 显示对应文件的描述
        for f in hint_files:
            if f['name'] == target_file:
                renpy.say(None, f['description'])
                break
    if target_file == "算了":
        return
    menu:
        "你要创建还是删除[target_file]?"
        "创建":
            $ create_hint_file(target_file)
        "删除":
            $ delete_hint_file(target_file)
    "完成了"
    return

label create_nomedia_files:
    python:
        import os
        def create_nomedia_recursive(root_path):
            """在指定路径及其所有子文件夹中创建.nomedia文件"""
            try:
                nomedia_count = 0
                for dirpath, dirnames, filenames in os.walk(root_path):
                    nomedia_file = os.path.join(dirpath, '.nomedia')
                    if not os.path.exists(nomedia_file):
                        with open(nomedia_file, 'w') as f:
                            pass
                        nomedia_count += 1
                return nomedia_count
            except Exception as e:
                return -1

        base_path = ANDROID_MASBASE
        result = create_nomedia_recursive(base_path)

    if result > 0:
        m "成功在 [result] 个文件夹中创建了.nomedia文件！"
    elif result == 0:
        m ".nomedia文件已经存在于所有文件夹中了。"
    else:
        m "创建.nomedia文件时发生错误。"
    return

init 5 python:  
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="hide_all_dev",
            category=["维护功能"],
            prompt="隐藏所有开发者话题",
            pool=True,
            unlocked=True
        )
    )   
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="show_all_dev",
            category=["维护功能"],
            prompt="显示所有开发者话题",
            pool=True,
            unlocked=True
        )
    )  
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="install_submods",
            category=["维护功能"],
            prompt="子模组安装&卸载",
            pool=True,
            unlocked=True
        )
    )  
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="create_hint_file",
            category=["维护功能"],
            prompt="创建标识文件",
            pool=True,
            unlocked=True
        )
    )
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="create_nomedia_files",
            category=["维护功能"],
            prompt="创建.nomedia文件",
            pool=True,
            unlocked=True
        )
    )
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="install_datapack",
            category=["维护功能"],
            prompt="安装数据包",
            pool=True,
            unlocked=True
        )
    )

label install_datapack:
    $ spread_json()
    "OK"
    return

init -2000 python:
    import store
    def load_persistent(filename):
        from renpy.compat.pickle import dump, dumps, loads
        import zlib

        if not os.path.exists(filename):
            return None
        try:
            with open(filename, "rb") as f:
                do = zlib.decompressobj()
                s = do.decompress(f.read())

        except Exception as e:
            raise e
        return loads(s)

    import os
    if os.path.exists(os.path.join(ANDROID_MASBASE, 'saves', 'persistent')) and not ANDROID_SAVEDIR_CHANGED:
        try:
#            newpersistent = load_persistent(os.path.join(ANDROID_MASBASE, 'saves', 'persistent'))
#            renpy.game.persistent = newpersistent
#            renpy.save_persistent()
            import shutil
            shutil.copyfile(os.path.join(ANDROID_MASBASE,"saves", "persistent"), renpy.config.savedir + "/persistent")
            android_toast("导入存档成功")
            os.remove(os.path.join(ANDROID_MASBASE, 'saves', 'persistent'))
        except Exception as e:
            import time
            android_toast("导入存档失败")
            store.mas_per_check.early_log.error("Error while loading persistent data: {}".format(e))
            os.rename(os.path.join(ANDROID_MASBASE, 'saves', 'persistent'), os.path.join(ANDROID_MASBASE, 'saves', 'persistent_bad{}'.format(time.time())))


label p_old_savefiles_location_check:
    python:
        import os
        import shutil

        # 检查旧存档路径
        # 如果在/sdcard/Android/data/and.sirp.masmobile/files/saves发现了persistent文件，就询问是否导入存档文件。
        # 如果同意，就把这个文件夹下所有内容剪贴至renpy.config.savedir

        old_savedir = "/sdcard/Android/data/and.sirp.masmobile/files/saves"
        persistent_file = os.path.join(old_savedir, "persistent")
        should_import = False

        # 检查旧存档路径是否存在且包含persistent文件
        if os.path.exists(old_savedir) and os.path.exists(persistent_file):
            should_import = True

    if should_import:
        "在先前的版本中, 我们调整了存档位置以防止因为误卸载导致存档丢失。"
        "存档位置已被修改, 你是否想要导入先前的存档?{nw}"
        menu:
            "存档位置已被修改, 你是否想要导入先前的存档?{fast}"
            "是，导入存档":
                python:
                    try:
                        # 获取当前的存档目录
                        current_savedir = renpy.config.savedir

                        # 确保目标目录存在
                        if not os.path.exists(current_savedir):
                            os.makedirs(current_savedir, exist_ok=True)

                        # 移动旧存档目录下的所有文件到新位置
                        for item in os.listdir(old_savedir):
                            src_path = os.path.join(old_savedir, item)
                            dst_path = os.path.join(current_savedir, item)

                            # 如果目标文件已存在，先删除
                            if os.path.exists(dst_path):
                                if os.path.isfile(dst_path):
                                    os.remove(dst_path)
                                elif os.path.isdir(dst_path):
                                    shutil.rmtree(dst_path)

                            # 移动文件或目录
                            shutil.move(src_path, dst_path)

                        # 尝试删除空的旧目录
                        try:
                            os.rmdir(old_savedir)
                        except:
                            pass

                        import logging
                        logging.info(f"Successfully coped saves from {old_savedir} to {current_savedir}")
                        renpy.quit()
                    except Exception as e:
                        import logging
                        logging.error(f"Failed to import saves: {e}")

            "否，跳过":
                pass

    return
