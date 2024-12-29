python early:    
    ANDROID_MASBASE = "/storage/emulated/0/MAS/"
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
    p_perms = [
        "android.permission.INTERNET",# 开启联网权限 用于备份
        "android.permission.WRITE_EXTERNAL_STORAGE", # 读写权限
        "android.permission.READ_EXTERNAL_STORAGE",
        #"android.permission.MANAGE_EXTERNAL_STORAGE"
    ]
    build.android_permissions = p_perms
    # 权限请求
    p_perm_dict = {}
    def req_perm():
        for i in p_perms:
            if not renpy.check_permission(i):
                try:
                    p_perm_dict[i] = renpy.request_permission(i)
                    if not p_perm_dict[i]:
                        android_toast("无法申请权限 {}".format(i))
                except Exception:
                    android_toast("无法申请权限 {}，请手动授予权限！".format(i))
        pass
    def p_raise():
        raise Exception("Raise Exception for Debugging")
    req_perm()
    if renpy.android:
        android_toast("正在加载游戏文件...")
        restart = gameSyncer.sync()
        if gameSyncer.rpy_deleted:
            android_toast("有rpyc被删除, 可能需要手动重启")
        if gameSyncer.restart_required:
            android_toast("检测到文件修改, 正在重载脚本")
init python:
    import os
    @store.mas_submod_utils.functionplugin("ch30_preloop", priority=-10000)
    def _gamesync_restartcheck():
        if gameSyncer.restart_required:
            renpy.full_restart()
            renpy.reload_script()
    def mkdir(path):
        if not os.path.exists(path):
            os.makedirs(path)
    def extract_file(file):
        # 解压文件, 仅限于game目录下的文件
        if not renpy.loadable(file):
            store.mas_utils.mas_log.error(f"extract_file: 无法释放文件，因为无法加载'{file}'")
            return
        
        # 定义目标路径
        target_path = os.path.join("/storage/emulated/0/MAS/game", file)
        target_dir = os.path.dirname(target_path)

        # 创建目标目录（如果不存在）
        os.makedirs(target_dir, exist_ok=True)

        # 写入文件
        with open(target_path, "wb") as f:
            f.write(renpy.file(file).read())

    def firstrun_spread():
        spread_json()
        android_toast("数据文件已安装, 推荐重启游戏再游玩")

    def spread_json():
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_bisexualpride.json", "wb").write(renpy.file("anonymioo_acs_ribbon_bisexualpride.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_blackandwhite.json", "wb").write(renpy.file("anonymioo_acs_ribbon_blackandwhite.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_bronze.json", "wb").write(renpy.file("anonymioo_acs_ribbon_bronze.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_brown.json", "wb").write(renpy.file("anonymioo_acs_ribbon_brown.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_gradient.json", "wb").write(renpy.file("anonymioo_acs_ribbon_gradient.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_gradient_lowpoly.json", "wb").write(renpy.file("anonymioo_acs_ribbon_gradient_lowpoly.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_gradient_lowpoly.json", "wb").write(renpy.file("anonymioo_acs_ribbon_gradient_lowpoly.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_gradient_rainbow.json", "wb").write(renpy.file("anonymioo_acs_ribbon_gradient_rainbow.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_polkadots_whiteonred.json", "wb").write(renpy.file("anonymioo_acs_ribbon_polkadots_whiteonred.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_starsky_black.json", "wb").write(renpy.file("anonymioo_acs_ribbon_starsky_black.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_starsky_red.json", "wb").write(renpy.file("anonymioo_acs_ribbon_starsky_red.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_striped_blueandwhite.json", "wb").write(renpy.file("anonymioo_acs_ribbon_striped_blueandwhite.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_striped_pinkandwhite.json", "wb").write(renpy.file("anonymioo_acs_ribbon_striped_pinkandwhite.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/anonymioo_acs_ribbon_transexualpride.json", "wb").write(renpy.file("anonymioo_acs_ribbon_transexualpride.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/bellmandi86_acs_hairclip_crescentmoon.json", "wb").write(renpy.file("bellmandi86_acs_hairclip_crescentmoon.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/bellmandi86_acs_hairclip_ghost.json", "wb").write(renpy.file("bellmandi86_acs_hairclip_ghost.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/bellmandi86_acs_hairclip_pumpkin.json", "wb").write(renpy.file("bellmandi86_acs_hairclip_pumpkin.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/bellmandi96_acs_hairclip_bat.json", "wb").write(renpy.file("bellmandi96_acs_hairclip_bat.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/echo_hair_downshort.json", "wb").write(renpy.file("echo_hair_downshort.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/echo_hair_ponytailshort.json", "wb").write(renpy.file("echo_hair_ponytailshort.json").read())
        
        
        
        
        
        
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/finale_clothes_jacket_brown.json", "wb").write(renpy.file("finale_clothes_jacket_brown.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/finale_clothes_shirt_blue.json", "wb").write(renpy.file("finale_clothes_shirt_blue.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/finale_hoodie_green.json", "wb").write(renpy.file("finale_hoodie_green.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/jmo_acs_hairclip_cherry.json", "wb").write(renpy.file("jmo_acs_hairclip_cherry.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/jmo_acs_hairclip_heart.json", "wb").write(renpy.file("jmo_acs_hairclip_heart.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/jmo_acs_hairclip_musicnote.json", "wb").write(renpy.file("jmo_acs_hairclip_musicnote.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/lanvallime_acs_ribbon_coffee.json", "wb").write(renpy.file("lanvallime_acs_ribbon_coffee.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/lanvallime_acs_ribbon_gold.json", "wb").write(renpy.file("lanvallime_acs_ribbon_gold.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/lanvallime_acs_ribbon_hot_pink.json", "wb").write(renpy.file("lanvallime_acs_ribbon_hot_pink.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/lanvallime_acs_ribbon_lilac.json", "wb").write(renpy.file("lanvallime_acs_ribbon_lilac.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/lanvallime_acs_ribbon_lime_green.json", "wb").write(renpy.file("lanvallime_acs_ribbon_lime_green.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/lanvallime_acs_ribbon_navy_blue.json", "wb").write(renpy.file("lanvallime_acs_ribbon_navy_blue.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/lanvallime_acs_ribbon_orange.json", "wb").write(renpy.file("lanvallime_acs_ribbon_orange.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/lanvallime_acs_ribbon_royal_purple.json", "wb").write(renpy.file("lanvallime_acs_ribbon_royal_purple.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/lanvallime_acs_ribbon_sky_blue.json", "wb").write(renpy.file("lanvallime_acs_ribbon_sky_blue.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/mas_hair_bun.json", "wb").write(renpy.file("mas_hair_bun.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/mocca_bun_blackandwhitestripedpullover.json", "wb").write(renpy.file("mocca_bun_blackandwhitestripedpullover.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/multimokia_acs_bow_black.json", "wb").write(renpy.file("multimokia_acs_bow_black.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_acs_hairflower_pink.json", "wb").write(renpy.file("orcaramelo_acs_hairflower_pink.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_acs_sakuya_izayoi_headband.json", "wb").write(renpy.file("orcaramelo_acs_sakuya_izayoi_headband.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_acs_sakuya_izayoi_strandbow.json", "wb").write(renpy.file("orcaramelo_acs_sakuya_izayoi_strandbow.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_acs_twinribbon_blue.json", "wb").write(renpy.file("orcaramelo_acs_twinribbon_blue.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_acs_twinribbon_green.json", "wb").write(renpy.file("orcaramelo_acs_twinribbon_green.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_acs_twinribbon_pink.json", "wb").write(renpy.file("orcaramelo_acs_twinribbon_pink.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_acs_twinribbon_yellow.json", "wb").write(renpy.file("orcaramelo_acs_twinribbon_yellow.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_clothes_bikini_shell.json", "wb").write(renpy.file("orcaramelo_clothes_bikini_shell.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_clothes_hatsune_miku.json", "wb").write(renpy.file("orcaramelo_clothes_hatsune_miku.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_clothes_sakuya_izayoi.json", "wb").write(renpy.file("orcaramelo_clothes_sakuya_izayoi.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_clothes_sweater_shoulderless.json", "wb").write(renpy.file("orcaramelo_clothes_sweater_shoulderless.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_hair_bunbraid.json", "wb").write(renpy.file("orcaramelo_hair_bunbraid.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_hair_ponytailbraid.json", "wb").write(renpy.file("orcaramelo_hair_ponytailbraid.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_hair_twinbun.json", "wb").write(renpy.file("orcaramelo_hair_twinbun.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_hair_twintails.json", "wb").write(renpy.file("orcaramelo_hair_twintails.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_hair_usagi.json", "wb").write(renpy.file("orcaramelo_hair_usagi.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_hatsune_miku_headset.json", "wb").write(renpy.file("orcaramelo_hatsune_miku_headset.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/orcaramelo_hatsune_miku_twinsquares.json", "wb").write(renpy.file("orcaramelo_hatsune_miku_twinsquares.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/retroadamshow_acs_bow_blue_retro.json", "wb").write(renpy.file("retroadamshow_acs_bow_blue_retro.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/retroadamshow_acs_bow_emerald_retro.json", "wb").write(renpy.file("retroadamshow_acs_bow_emerald_retro.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/retroadamshow_acs_bow_retro.json", "wb").write(renpy.file("retroadamshow_acs_bow_retro.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/sirnimblybottoms_acs_heart_choker.json", "wb").write(renpy.file("sirnimblybottoms_acs_heart_choker.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/trilasent_acs_choker_flowered.json", "wb").write(renpy.file("trilasent_acs_choker_flowered.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/trilasent_acs_choker_simple.json", "wb").write(renpy.file("trilasent_acs_choker_simple.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_black.json", "wb").write(renpy.file("velius94_acs_ribbon_black.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_blue.json", "wb").write(renpy.file("velius94_acs_ribbon_blue.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_dark_purple.json", "wb").write(renpy.file("velius94_acs_ribbon_dark_purple.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_def.json", "wb").write(renpy.file("velius94_acs_ribbon_def.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_emerald.json", "wb").write(renpy.file("velius94_acs_ribbon_emerald.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_gray.json", "wb").write(renpy.file("velius94_acs_ribbon_gray.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_green.json", "wb").write(renpy.file("velius94_acs_ribbon_green.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_light_purple.json", "wb").write(renpy.file("velius94_acs_ribbon_light_purple.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_peach.json", "wb").write(renpy.file("velius94_acs_ribbon_peach.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_pink.json", "wb").write(renpy.file("velius94_acs_ribbon_pink.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_platinum.json", "wb").write(renpy.file("velius94_acs_ribbon_platinum.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_red.json", "wb").write(renpy.file("velius94_acs_ribbon_red.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_ruby.json", "wb").write(renpy.file("velius94_acs_ribbon_ruby.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_sapphire.json", "wb").write(renpy.file("velius94_acs_ribbon_sapphire.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_silver.json", "wb").write(renpy.file("velius94_acs_ribbon_silver.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_teal.json", "wb").write(renpy.file("velius94_acs_ribbon_teal.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_wine.json", "wb").write(renpy.file("velius94_acs_ribbon_wine.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_acs_ribbon_yellow.json", "wb").write(renpy.file("velius94_acs_ribbon_yellow.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_clothes_dress_whitenavyblue.json", "wb").write(renpy.file("velius94_clothes_dress_whitenavyblue.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/velius94_clothes_shirt_pink.json", "wb").write(renpy.file("velius94_clothes_shirt_pink.json").read())
        extract_file("mod_assets/monika/cg/o31rcg")
        extract_file("mod_assets/monika/cg/o31mcg")
        extract_file("mod_assets/monika/cg/o31mcg") 
        extract_file("mod_assets/location/special/our_reality")   
        extract_file("mod_assets/monika/mbase")   
        extract_file("mod_assets/monika/NjM2ODZmNjM2ZjZjNjE3NDY1NzM=")
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/finale_clothes_green_dress.json", "wb").write(renpy.file("finale_clothes_green_dress.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/finale_clothes_putonahappyface_shirt.json", "wb").write(renpy.file("finale_clothes_putonahappyface_shirt.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/finale_clothes_shirt_resthere.json", "wb").write(renpy.file("finale_clothes_shirt_resthere.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/finale_clothes_tanktop.json", "wb").write(renpy.file("finale_clothes_tanktop.json").read())
        extract_file("mod_assets/games/piano/songs/happybirthday.json")
        extract_file("mod_assets/games/piano/songs/yourreality.json")
        extract_file("mod_assets/games/chess/stockfish-8-arm64-v8a")
        extract_file("python-packages/certifi/cacert.pem")
        extract_file("audio.rpa")
        
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/briaryoung_acs_front_bow_black.json", "wb").write(renpy.file("briaryoung_acs_front_bow_black.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/briaryoung_clothes_shuchiin_academy_uniform.json", "wb").write(renpy.file("briaryoung_clothes_shuchiin_academy_uniform.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/briaryoung_hair_down_straight_bangs.json", "wb").write(renpy.file("briaryoung_hair_down_straight_bangs.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/finale_clothes_sweatervest_blue.json", "wb").write(renpy.file("finale_clothes_sweatervest_blue.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/finale_clothes_turtleneck_sweater_beige.json", "wb").write(renpy.file("finale_clothes_turtleneck_sweater_beige.json").read())
        #open("/storage/emulated/0/MAS/game/mod_assets/monika/j/multimokia_clothes_wine_asymmetrical_pullover.json", "wb").write(renpy.file("multimokia_clothes_wine_asymmetrical_pullover.json").read())
        gameSyncer.sync()


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
    "正在导出存档"
    "注意：只导出自动备份的文件（.bak）文件"
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
    if os.path.exists(os.path.join(ANDROID_MASBASE, 'saves', 'persistent')):
        try:
            android_toast("导入存档成功")
            store.persistent = load_persistent(os.path.join(ANDROID_MASBASE, 'saves', 'persistent'))
            os.remove(os.path.join(ANDROID_MASBASE, 'saves', 'persistent'))
        except Exception as e:
            android_toast("导入存档失败")
            store.mas_per_check.early_log.error("Error while loading persistent data: {}".format(e))
            os.rename(os.path.join(ANDROID_MASBASE, 'saves', 'persistent'), os.path.join(ANDROID_MASBASE, 'saves', 'persistent_bad'))

