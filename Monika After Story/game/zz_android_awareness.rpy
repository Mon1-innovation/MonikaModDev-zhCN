## Android awareness bridge.
##
## Ren'Py asks Java for the current awareness state directly. The bridge does
## does not save or read a mirrored state file.

init -10 python:
    if persistent._mas_awareness_enabled is None:
        persistent._mas_awareness_enabled = False

    if persistent._mas_awareness_permits_accepted is None:
        persistent._mas_awareness_permits_accepted = False

    if persistent._mas_awareness_last_app_mention is None:
        persistent._mas_awareness_last_app_mention = {}

    if persistent._mas_awareness_last_music_track is None:
        persistent._mas_awareness_last_music_track = ""


init -5 python:
    import json
    import os
    import time

    _MAS_AWARENESS_ENABLED_PATH = "/storage/emulated/0/Monika After Story/log/.awareness_enabled"
    _mas_awareness_last_state_error = ""
    _mas_awareness_last_state_parsed_type = ""
    _mas_awareness_last_state_raw = ""
    _mas_awareness_last_state_raw_type = ""

    def _mas_awareness_log(message):
        try:
            store.mas_utils.mas_log.info("[MAS_AWARENESS] " + str(message))
        except Exception:
            print("[MAS_AWARENESS] " + str(message))

    MAS_APP_CATEGORIES = {
        "YouTube": "video",
        "Netflix": "video",
        "Twitch": "video",
        "Prime Video": "video",
        "Disney+": "video",
        "Crunchyroll": "video",
        "Spotify": "music",
        "YouTube Music": "music",
        "Apple Music": "music",
        "Amazon Music": "music",
        "SoundCloud": "music",
        "Deezer": "music",
        "Instagram": "social",
        "Twitter": "social",
        "X": "social",
        "TikTok": "social",
        "Facebook": "social",
        "Reddit": "social",
        "Tumblr": "social",
        "Threads": "social",
        "WhatsApp": "messaging",
        "Discord": "messaging",
        "Telegram": "messaging",
        "Messenger": "messaging",
        "Signal": "messaging",
        "Line": "messaging",
        "Chrome": "browser",
        "Firefox": "browser",
        "Samsung Internet": "browser",
        "Opera": "browser",
        "Brave": "browser",
        "Edge": "browser",
        "Steam": "gaming",
        "Google Play Games": "gaming",
    }

    def _mas_awareness_as_python_string(value):
        if value is None:
            return ""

        try:
            if hasattr(value, "toString"):
                return str(value.toString())
        except Exception:
            pass

        try:
            return str(value)
        except Exception:
            return ""

    def _mas_awareness_is_string(value):
        try:
            return isinstance(value, basestring)
        except NameError:
            return isinstance(value, str)

    def _mas_awareness_is_dict(value):
        return (
            hasattr(value, "get")
            and hasattr(value, "keys")
            and hasattr(value, "__getitem__")
        )

    def _mas_awareness_is_list(value):
        return (
            not _mas_awareness_is_string(value)
            and hasattr(value, "__iter__")
            and hasattr(value, "__len__")
            and hasattr(value, "__getitem__")
            and not _mas_awareness_is_dict(value)
        )

    def _mas_awareness_get_latest_app(apps):
        latest_app = None
        latest_timestamp = -1

        for app in apps:
            if not _mas_awareness_is_dict(app):
                continue

            try:
                app_timestamp = int(app.get("last_used", 0) or 0)
            except Exception:
                app_timestamp = 0

            if latest_app is None or app_timestamp >= latest_timestamp:
                latest_app = app
                latest_timestamp = app_timestamp

        return latest_app

    def mas_awareness_read_state():
        global _mas_awareness_last_state_error
        global _mas_awareness_last_state_parsed_type
        global _mas_awareness_last_state_raw
        global _mas_awareness_last_state_raw_type

        _mas_awareness_last_state_error = ""
        _mas_awareness_last_state_parsed_type = ""
        _mas_awareness_last_state_raw = ""
        _mas_awareness_last_state_raw_type = ""

        if not renpy.android:
            _mas_awareness_last_state_error = "renpy.android is false"
            return None

        try:
            from jnius import autoclass as _mas_awareness_autoclass

            try:
                PythonActivity = _mas_awareness_autoclass("org.renpy.android.PythonSDLActivity")
            except Exception:
                PythonActivity = _mas_awareness_autoclass("org.renpy.android.PythonActivity")

            AwarenessService = _mas_awareness_autoclass("com.monikaafterstory.tec.es.AwarenessService")
            content = AwarenessService.buildState(PythonActivity.mActivity)
            _mas_awareness_last_state_raw_type = type(content).__name__
            if not content:
                _mas_awareness_last_state_error = "Java buildState returned empty content"
                _mas_awareness_log(_mas_awareness_last_state_error)
                return None

            content_text = _mas_awareness_as_python_string(content).strip()
            _mas_awareness_last_state_raw = content_text[:500]
            _mas_awareness_log(
                "Java state raw_type={0}, raw_len={1}, raw={2}".format(
                    _mas_awareness_last_state_raw_type,
                    len(content_text),
                    content_text
                )
            )
            if not content_text:
                _mas_awareness_last_state_error = "Java buildState returned blank text"
                _mas_awareness_log(_mas_awareness_last_state_error)
                return None

            try:
                parsed_state = json.loads(content_text)
                if _mas_awareness_is_string(parsed_state):
                    _mas_awareness_log("Java state was JSON-encoded twice; parsing inner string.")
                    parsed_state = json.loads(parsed_state)

                _mas_awareness_last_state_parsed_type = type(parsed_state).__name__

                if not _mas_awareness_is_dict(parsed_state):
                    _mas_awareness_last_state_error = (
                        "Java state parsed as non-dict: "
                        + _mas_awareness_last_state_parsed_type
                    )
                    _mas_awareness_log(_mas_awareness_last_state_error)
                    return None

                _mas_awareness_log("Java state parsed as dict successfully")
                return parsed_state

            except Exception as e:
                _mas_awareness_last_state_error = "json.loads failed: " + str(e)
                _mas_awareness_log("Error parsing Java state: " + str(e))
                return None

        except Exception as e:
            _mas_awareness_last_state_error = str(e)
            _mas_awareness_log("Error reading Java state: " + str(e))
            return None

    def mas_awareness_get_last_state_debug():
        return {
            "error": _mas_awareness_last_state_error,
            "parsed_type": _mas_awareness_last_state_parsed_type,
            "raw": _mas_awareness_last_state_raw,
            "raw_type": _mas_awareness_last_state_raw_type,
        }

    def mas_awareness_get_recent_apps():
        state = mas_awareness_read_state()
        if not state:
            return []

        apps = state.get("recent_apps", [])
        if _mas_awareness_is_list(apps):
            return apps

        return []

    def mas_awareness_get_most_recent_app():
        apps = mas_awareness_get_recent_apps()
        return _mas_awareness_get_latest_app(apps)

    def mas_awareness_get_app_category(app_label):
        return MAS_APP_CATEGORIES.get(app_label, "unknown")

    def mas_awareness_has_permission(perm_type):
        state = mas_awareness_read_state()
        if not state:
            return False

        perms = state.get("permissions", {})
        if not _mas_awareness_is_dict(perms):
            return False

        return bool(perms.get(perm_type, False))

    def mas_awareness_should_react_app(app_label):
        if not app_label:
            return False

        history = persistent._mas_awareness_last_app_mention
        if not _mas_awareness_is_dict(history):
            history = {}
            persistent._mas_awareness_last_app_mention = history

        return (time.time() - history.get(app_label, 0)) >= 21600

    def mas_awareness_mark_app_reacted(app_label):
        if not _mas_awareness_is_dict(persistent._mas_awareness_last_app_mention):
            persistent._mas_awareness_last_app_mention = {}

        persistent._mas_awareness_last_app_mention[app_label] = time.time()

    def mas_awareness_write_enabled_state(enabled=None):
        if enabled is None:
            enabled = persistent._mas_awareness_enabled

        try:
            enabled_dir = os.path.dirname(_MAS_AWARENESS_ENABLED_PATH)
            if not os.path.exists(enabled_dir):
                os.makedirs(enabled_dir)

            with open(_MAS_AWARENESS_ENABLED_PATH, "w") as enabled_file:
                enabled_file.write("1" if enabled else "0")

        except Exception as e:
            print("[MAS_AWARENESS] Error writing enabled state: " + str(e))

    store.mas_awareness_read_state = mas_awareness_read_state
    store.mas_awareness_get_last_state_debug = mas_awareness_get_last_state_debug
    store.mas_awareness_get_recent_apps = mas_awareness_get_recent_apps
    store.mas_awareness_get_most_recent_app = mas_awareness_get_most_recent_app
    store.mas_awareness_get_app_category = mas_awareness_get_app_category
    store.mas_awareness_has_permission = mas_awareness_has_permission
    store.mas_awareness_should_react_app = mas_awareness_should_react_app
    store.mas_awareness_mark_app_reacted = mas_awareness_mark_app_reacted
    store.mas_awareness_write_enabled_state = mas_awareness_write_enabled_state
    store._mas_awareness_is_dict = _mas_awareness_is_dict
    store._mas_awareness_is_list = _mas_awareness_is_list
    store._mas_awareness_get_latest_app = _mas_awareness_get_latest_app


init 5 python:
    if mas_android_backend_available and renpy.android:

        def mas_awareness_request_usage_permission():
            try:
                try:
                    PythonActivity = autoclass("org.renpy.android.PythonSDLActivity")
                except Exception:
                    PythonActivity = autoclass("org.renpy.android.PythonActivity")

                AwarenessService = autoclass("com.monikaafterstory.tec.es.AwarenessService")
                AwarenessService.requestUsagePermission(PythonActivity.mActivity)

            except Exception as e:
                print("[MAS_AWARENESS] requestUsagePermission error: " + str(e))

        def mas_awareness_refresh_state():
            return mas_awareness_read_state()

        def mas_awareness_check_and_open_permits():
            mas_awareness_request_usage_permission()

    else:

        def mas_awareness_request_usage_permission():
            print("[MAS_AWARENESS] (Simulated) Opening Usage Access settings")

        def mas_awareness_refresh_state():
            print("[MAS_AWARENESS] (Simulated) Reading awareness state")
            return mas_awareness_read_state()

        def mas_awareness_check_and_open_permits():
            print("[MAS_AWARENESS] (Simulated) Opening awareness permits")

    store.mas_awareness_request_usage_permission = mas_awareness_request_usage_permission
    store.mas_awareness_refresh_state = mas_awareness_refresh_state
    store.mas_awareness_check_and_open_permits = mas_awareness_check_and_open_permits

    def mas_awareness_startup_sync():
        mas_awareness_write_enabled_state()

    if renpy.android:
        config.start_callbacks.append(mas_awareness_startup_sync)


init 10 python:
    import random as _mas_awareness_random

    MAS_AWARENESS_APP_MESSAGES = {
        "video": [
            _("I noticed you were using {app}. Were you watching something interesting?"),
            _("Oh, you were on {app}? I hope you found a good video."),
            _("I saw you opened {app}. What were you watching?"),
        ],
        "music": [
            _("I see you were on {app}. Listening to something good?"),
            _("Oh, {app} was open. I wish I could listen along with you."),
            _("You were using {app}, weren't you? I hope it was a good playlist."),
        ],
        "social": [
            _("I noticed you were scrolling through {app}. Did you see anything fun?"),
            _("Oh, you were on {app}? I hope you had a good time there."),
            _("I saw you opened {app}. Don't forget about me, okay?"),
        ],
        "messaging": [
            _("I see you were chatting on {app}. I hope they're good friends."),
            _("Oh, you were on {app}? Who were you talking to?"),
            _("I noticed {app} was open. It's nice that you keep in touch with people."),
        ],
        "browser": [
            _("I saw you were browsing on {app}. Find anything interesting?"),
            _("Oh, you had {app} open. What were you looking up?"),
            _("I noticed you were using {app}. Doing some research?"),
        ],
        "gaming": [
            _("I see you were playing something on {app}. Was it fun?"),
            _("Oh, {app} was open? I hope you had a good time... but I'm glad you came back to me."),
            _("I noticed you were on {app}. Were you gaming without me?"),
        ],
        "unknown": [
            _("I noticed you were using {app}. What were you up to?"),
            _("Oh, you had {app} open. I'm curious what you were doing."),
            _("I saw {app} was active on your phone. Everything okay?"),
        ],
    }

    def mas_awareness_get_app_reaction():
        if not persistent._mas_awareness_enabled:
            return None

        app = mas_awareness_get_most_recent_app()
        if not app:
            return None

        app_label = app.get("label", "")
        if not app_label or not mas_awareness_should_react_app(app_label):
            return None

        category = mas_awareness_get_app_category(app_label)
        messages = MAS_AWARENESS_APP_MESSAGES.get(category, MAS_AWARENESS_APP_MESSAGES["unknown"])
        message = _mas_awareness_random.choice(messages).replace("{app}", app_label)

        mas_awareness_mark_app_reacted(app_label)
        return message

    store.mas_awareness_get_app_reaction = mas_awareness_get_app_reaction


label mas_greeting_awareness_app:
    python:
        _mas_awareness_app_message = mas_awareness_get_app_reaction()

    if _mas_awareness_app_message:
        m 1eua "[_mas_awareness_app_message]"

    return


label mas_greeting_awareness_music:
    return
