## Android awareness bridge.
##
## Java writes a small JSON snapshot to /log/.awareness; this module reads it
## and exposes optional app-context reactions to Ren'Py.

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

    _MAS_AWARENESS_SNAPSHOT_PATH = "/storage/emulated/0/Monika After Story/log/.awareness"
    _MAS_AWARENESS_ENABLED_PATH = "/storage/emulated/0/Monika After Story/log/.awareness_enabled"
    _MAS_AWARENESS_POLL_INTERVAL = 10
    _mas_awareness_last_snapshot = None
    _mas_awareness_last_read_time = 0

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

    def mas_awareness_read_snapshot():
        global _mas_awareness_last_snapshot, _mas_awareness_last_read_time

        now = time.time()
        if now - _mas_awareness_last_read_time < _MAS_AWARENESS_POLL_INTERVAL:
            return _mas_awareness_last_snapshot

        _mas_awareness_last_read_time = now

        try:
            if not os.path.exists(_MAS_AWARENESS_SNAPSHOT_PATH):
                return None

            with open(_MAS_AWARENESS_SNAPSHOT_PATH, "r") as snapshot_file:
                content = snapshot_file.read().strip()

            if not content:
                return None

            _mas_awareness_last_snapshot = json.loads(content)
            return _mas_awareness_last_snapshot

        except Exception as e:
            print("[MAS_AWARENESS] Error reading snapshot: " + str(e))
            return None

    def mas_awareness_get_recent_apps():
        snapshot = mas_awareness_read_snapshot()
        if not snapshot:
            return []

        apps = snapshot.get("recent_apps", [])
        if isinstance(apps, list):
            return apps

        return []

    def mas_awareness_get_most_recent_app():
        apps = mas_awareness_get_recent_apps()
        return apps[-1] if apps else None

    def mas_awareness_get_app_category(app_label):
        return MAS_APP_CATEGORIES.get(app_label, "unknown")

    def mas_awareness_has_permission(perm_type):
        snapshot = mas_awareness_read_snapshot()
        if not snapshot:
            return False

        perms = snapshot.get("permissions", {})
        if not isinstance(perms, dict):
            return False

        return bool(perms.get(perm_type, False))

    def mas_awareness_should_react_app(app_label):
        if not app_label:
            return False

        history = persistent._mas_awareness_last_app_mention
        if not isinstance(history, dict):
            history = {}
            persistent._mas_awareness_last_app_mention = history

        return (time.time() - history.get(app_label, 0)) >= 21600

    def mas_awareness_mark_app_reacted(app_label):
        if not isinstance(persistent._mas_awareness_last_app_mention, dict):
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

    store.mas_awareness_read_snapshot = mas_awareness_read_snapshot
    store.mas_awareness_get_recent_apps = mas_awareness_get_recent_apps
    store.mas_awareness_get_most_recent_app = mas_awareness_get_most_recent_app
    store.mas_awareness_get_app_category = mas_awareness_get_app_category
    store.mas_awareness_has_permission = mas_awareness_has_permission
    store.mas_awareness_should_react_app = mas_awareness_should_react_app
    store.mas_awareness_mark_app_reacted = mas_awareness_mark_app_reacted
    store.mas_awareness_write_enabled_state = mas_awareness_write_enabled_state


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

        def mas_awareness_force_snapshot():
            try:
                try:
                    PythonActivity = autoclass("org.renpy.android.PythonSDLActivity")
                except Exception:
                    PythonActivity = autoclass("org.renpy.android.PythonActivity")

                AwarenessService = autoclass("com.monikaafterstory.tec.es.AwarenessService")
                AwarenessService.writeSnapshot(PythonActivity.mActivity)

            except Exception as e:
                print("[MAS_AWARENESS] forceSnapshot error: " + str(e))

        def mas_awareness_check_and_open_permits():
            mas_awareness_force_snapshot()
            mas_awareness_request_usage_permission()

    else:

        def mas_awareness_request_usage_permission():
            print("[MAS_AWARENESS] (Simulated) Opening Usage Access settings")

        def mas_awareness_force_snapshot():
            print("[MAS_AWARENESS] (Simulated) Writing awareness snapshot")

        def mas_awareness_check_and_open_permits():
            print("[MAS_AWARENESS] (Simulated) Opening awareness permits")

    store.mas_awareness_request_usage_permission = mas_awareness_request_usage_permission
    store.mas_awareness_force_snapshot = mas_awareness_force_snapshot
    store.mas_awareness_check_and_open_permits = mas_awareness_check_and_open_permits

    def mas_awareness_startup_sync():
        mas_awareness_write_enabled_state()
        if persistent._mas_awareness_enabled:
            mas_awareness_force_snapshot()

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
