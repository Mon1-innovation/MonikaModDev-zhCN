init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_android_awareness_debug",
            category=["dev", "维护功能"],
            prompt="Android 感知调试",
            pool=True,
            unlocked=True
        )
    )

    def dev_android_awareness_push_random_wrs():
        wrs_candidates = [
            (ev_label, ev)
            for ev_label, ev in store.mas_windowreacts.windowreact_db.items()
            if ev is not None and ev.unlocked and renpy.has_label(ev_label)
        ]

        if not wrs_candidates:
            return None

        _dev_android_wrs_label, _dev_android_wrs_event = renpy.random.choice(wrs_candidates)
        MASEventList.queue(_dev_android_wrs_label)
        _dev_android_wrs_event.unlocked = False
        return _dev_android_wrs_label

    def _mas_dev_android_debug_json(value):
        import json

        try:
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        except Exception as e:
            return "<json error: {0}> {1}".format(e, value)

    def _mas_dev_android_debug_text(value):
        return str(value).replace("{", "{{").replace("}", "}}").replace("[", "[[")

    def _mas_dev_android_debug_call(func, fallback=None):
        try:
            return func()
        except Exception as e:
            return "<error: {0}>".format(e)

    def dev_android_awareness_collect_debug_values():
        _dev_android_state = (
            _mas_dev_android_debug_call(lambda: store.mas_awareness_read_state(), None)
            if hasattr(store, "mas_awareness_read_state")
            else None
        )
        _dev_android_state_debug = (
            _mas_dev_android_debug_call(lambda: store.mas_awareness_get_last_state_debug(), {})
            if hasattr(store, "mas_awareness_get_last_state_debug")
            else {}
        )

        if store._mas_awareness_is_dict(_dev_android_state):
            _dev_android_permissions = _dev_android_state.get("permissions", {})
            if not store._mas_awareness_is_dict(_dev_android_permissions):
                _dev_android_permissions = {}

            _dev_android_apps = _dev_android_state.get("recent_apps", [])
            if store._mas_awareness_is_list(_dev_android_apps) and _dev_android_apps:
                _dev_android_recent_app = store._mas_awareness_get_latest_app(_dev_android_apps)
            else:
                _dev_android_recent_app = None

            _dev_android_activity = _dev_android_state.get("mas_activity", {})
            if not store._mas_awareness_is_dict(_dev_android_activity):
                _dev_android_activity = {}

            _dev_android_usage_permission = bool(_dev_android_permissions.get("usage_stats", False))
            _dev_android_focused = bool(
                _dev_android_activity.get("resumed", False)
                and _dev_android_activity.get("has_window_focus", False)
            )
            _dev_android_state_keys = sorted(_dev_android_state.keys())
        else:
            _dev_android_usage_permission = False
            _dev_android_focused = False
            _dev_android_recent_app = None
            _dev_android_activity = {}
            _dev_android_state_keys = []

        _dev_android_active_window = _mas_dev_android_debug_call(mas_getActiveWindowHandle, "")

        return [
            ("renpy.android", bool(renpy.android)),
            ("Awareness 是否启用", bool(persistent._mas_awareness_enabled)),
            ("Usage Access 是否已授权", _dev_android_usage_permission),
            ("mas_getActiveWindowHandle()", _dev_android_active_window),
            ("mas_isFocused()", _dev_android_focused),
            ("最近前台 App", _mas_dev_android_debug_json(_dev_android_recent_app)),
            ("MAS activity", _mas_dev_android_debug_json(_dev_android_activity)),
            ("State keys", _mas_dev_android_debug_json(_dev_android_state_keys)),
            ("State bridge error", _dev_android_state_debug.get("error", "")),
            ("State parsed type", _dev_android_state_debug.get("parsed_type", "")),
            ("State raw type", _dev_android_state_debug.get("raw_type", "")),
        ]

    def dev_android_awareness_refresh_debug_values():
        store.dev_android_awareness_debug_values = [
            (label, _mas_dev_android_debug_text(value))
            for label, value in dev_android_awareness_collect_debug_values()
        ]

    store.dev_android_awareness_debug_values = []


screen dev_android_awareness_debug_screen():
    tag menu

    timer 1.0 action Function(dev_android_awareness_refresh_debug_values) repeat True

    use game_menu(_("Android 感知调试"), scroll="viewport"):
        style_prefix "check"

        vbox:
            spacing 10

            text _("这些值是从 Java 层即时读取的；完整 raw state 已写入 mas_log 和 logcat。")

            for _dev_android_debug_label, _dev_android_debug_value in store.dev_android_awareness_debug_values:
                vbox:
                    spacing 2
                    text _dev_android_debug_label
                    text _dev_android_debug_value size 20

label dev_android_awareness_debug:
    m 1eua "要运行哪一种 Android/window reaction 调试呢?{nw}"

    menu:
        "要运行哪一种 Android/window reaction 调试呢?{fast}"
        "显示 Android 感知数值":
            $ dev_android_awareness_refresh_debug_values()
            call screen dev_android_awareness_debug_screen
            return

        "随机推送一个 window reaction":
            $ _dev_android_wrs_queued = dev_android_awareness_push_random_wrs()
            if _dev_android_wrs_queued:
                m 1eub "已 queue window reaction: [_dev_android_wrs_queued]"
                m 1eua "这个话题结束后，它应该会优先播放。"
            else:
                m 1ekc "我没有找到可以推送的已解锁 window reaction。"
            return
