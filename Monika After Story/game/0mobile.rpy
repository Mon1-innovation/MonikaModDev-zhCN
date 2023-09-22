python early:
    renpy.config.version = renpy.config.version + ".Mobile"

python early:
    if renpy.android:
        p_debug = os.path.exists("/storage/emulated/0/MAS/debug.p")
    else:
        p_debug = True
    # debug
    renpy.config.developer = p_debug
    renpy.config.debug = p_debug
    renpy.config.console = p_debug
    p_perms = [
        "android.permission.INTERNET",# 开启联网权限 用于备份
        "android.permission.WRITE_EXTERNAL_STORAGE", # 读写权限
        "android.permission.READ_EXTERNAL_STORAGE"
    ]
    # 权限请求
    p_perm_dict = {}
    def req_perm():
        for i in p_perms:
            if not renpy.check_permission(i):
                p_perm_dict[i] = renpy.request_permission(i)
                p_perm_dict[i] = renpy.check_permission(i)
        pass
    def p_raise():
        raise Exception("Raise Exception for Debugging")
    req_perm()