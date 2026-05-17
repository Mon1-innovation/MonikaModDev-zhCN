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

    def dev_android_awareness_get_wrs_candidates():
        return [
            (ev_label, ev)
            for ev_label, ev in store.mas_windowreacts.windowreact_db.items()
            if ev is not None and ev.unlocked and renpy.has_label(ev_label)
        ]

    def dev_android_awareness_push_random_wrs():
        wrs_candidates = dev_android_awareness_get_wrs_candidates()

        if not wrs_candidates:
            return None

        _dev_android_wrs_label, _dev_android_wrs_event = renpy.random.choice(wrs_candidates)
        MASEventList.queue(_dev_android_wrs_label)
        _dev_android_wrs_event.unlocked = False
        return _dev_android_wrs_label

    def dev_android_awareness_clear_queue_push_random_wrs(count=5):
        wrs_candidates = [
            (ev_label, ev)
            for ev_label, ev in dev_android_awareness_get_wrs_candidates()
        ]
        _dev_android_wrs_labels = []

        while wrs_candidates and len(_dev_android_wrs_labels) < count:
            _dev_android_wrs_label, _dev_android_wrs_event = renpy.random.choice(wrs_candidates)
            wrs_candidates.remove((_dev_android_wrs_label, _dev_android_wrs_event))
            _dev_android_wrs_event.unlocked = False
            _dev_android_wrs_labels.append(_dev_android_wrs_label)

        if _dev_android_wrs_labels:
            persistent.event_list = []

            for _dev_android_wrs_label in _dev_android_wrs_labels:
                MASEventList.queue(_dev_android_wrs_label)

        return _dev_android_wrs_labels

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

    def dev_android_awareness_get_wrs_window_matches(active_window_handle):
        import re

        _dev_android_raw_matches = {}
        _dev_android_queueable_matches = []

        for ev_label, ev in store.mas_windowreacts.windowreact_db.items():
            if ev is None or not renpy.has_label(ev_label) or not ev.category:
                continue

            _dev_android_notif_group = ev.rules.get("notif-group", "<none>")
            _dev_android_pattern = ev.category[0]

            try:
                _dev_android_title_matches = bool(re.findall(_dev_android_pattern, active_window_handle))
            except Exception as e:
                _dev_android_title_matches = "<regex error: {0}>".format(e)

            if _dev_android_title_matches is True:
                _dev_android_raw_matches.setdefault(_dev_android_notif_group, []).append(ev_label)

                if (
                    Event._filterEvent(ev, unlocked=True, aff=store.mas_curr_affection)
                    and ev.checkConditional()
                    and ((not store.mas_globals.in_idle_mode) or (store.mas_globals.in_idle_mode and ev.show_in_idle))
                    and persistent._mas_windowreacts_windowreacts_enabled
                    and store.mas_windowreacts.can_show_notifs
                    and mas_notifsEnabledForGroup(_dev_android_notif_group)
                ):
                    _dev_android_queueable_matches.append(ev_label)

        return {
            "raw_group_matches": _dev_android_raw_matches,
            "queueable_events": _dev_android_queueable_matches,
        }

    def dev_android_awareness_get_event_list_labels():
        _dev_android_event_labels = []

        for _dev_android_event_item in persistent.event_list:
            if isinstance(_dev_android_event_item, tuple) and _dev_android_event_item:
                _dev_android_event_labels.append(_dev_android_event_item[0])
            else:
                _dev_android_event_labels.append(_dev_android_event_item)

        return _dev_android_event_labels

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
        _dev_android_wrs_matches = _mas_dev_android_debug_call(
            lambda: dev_android_awareness_get_wrs_window_matches(_dev_android_active_window),
            {}
        )
        if not isinstance(_dev_android_wrs_matches, dict):
            _dev_android_wrs_matches = {"error": _dev_android_wrs_matches}

        return [
            ("renpy.android", bool(renpy.android)),
            ("Awareness 是否启用", bool(persistent._mas_awareness_enabled)),
            ("Usage Access 是否已授权", _dev_android_usage_permission),
            ("mas_getActiveWindowHandle()", _dev_android_active_window),
            ("mas_isFocused()", _dev_android_focused),
            ("WRS 匹配检查错误", _dev_android_wrs_matches.get("error", "")),
            ("当前窗口匹配的通知组", _mas_dev_android_debug_json(_dev_android_wrs_matches.get("raw_group_matches", {}))),
            ("当前窗口可 queue 的 WRS", _mas_dev_android_debug_json(_dev_android_wrs_matches.get("queueable_events", []))),
            ("当前 EventList labels", _mas_dev_android_debug_json(dev_android_awareness_get_event_list_labels())),
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
    zorder 100

    timer 1.0 action Function(dev_android_awareness_refresh_debug_values) repeat True

    frame:
        xpos 20
        ypos 20
        xsize 560
        ymaximum 640
        background Solid("#111111AA")
        padding (10, 8)

        vbox:
            spacing 6

            hbox:
                xfill True
                text _("Android 感知调试") size 24
                textbutton _("X"):
                    xalign 1.0
                    action Hide("dev_android_awareness_debug_screen")

            text _("这些值是从 Java 层即时读取的；完整 raw state 已写入 mas_log 和 logcat。") size 18

            viewport:
                ymaximum 560
                mousewheel True
                draggable True

                vbox:
                    spacing 6

                    for _dev_android_debug_label, _dev_android_debug_value in store.dev_android_awareness_debug_values:
                        vbox:
                            spacing 1
                            text _dev_android_debug_label size 18
                            text _dev_android_debug_value size 16

label dev_android_awareness_debug:
    m 1eua "要运行哪一种 Android/window reaction 调试呢?{nw}"

    menu:
        "要运行哪一种 Android/window reaction 调试呢?{fast}"
        "显示 Android 感知数值":
            $ dev_android_awareness_refresh_debug_values()
            show screen dev_android_awareness_debug_screen
            m 1eua "我已经把 Android 感知数值显示在左上角的小悬浮窗了。"
            return

        "随机推送一个 window reaction":
            $ _dev_android_wrs_queued = dev_android_awareness_push_random_wrs()
            if _dev_android_wrs_queued:
                m 1eub "已 queue window reaction: [_dev_android_wrs_queued]"
                m 1eua "这个话题结束后，它应该会优先播放。"
            else:
                m 1ekc "我没有找到可以推送的已解锁 window reaction。"
            return

        "清空队列并随机推送 5 个 window reaction":
            $ _dev_android_wrs_queued = dev_android_awareness_clear_queue_push_random_wrs(5)
            if _dev_android_wrs_queued:
                $ _dev_android_wrs_queued_text = ", ".join(_dev_android_wrs_queued)
                m 1eub "已清空事件队列，并 queue window reactions: [_dev_android_wrs_queued_text]"
                m 1eua "这个话题结束后，它们应该会优先连续播放。"
            else:
                m 1ekc "我没有找到可以推送的已解锁 window reaction。"
            return
