## Android window reaction category compatibility.
##
## Android awareness exposes the foreground app as "<label> <package>" instead
## of a desktop window title, so desktop WRS keywords need mobile app matches.

init 20 python:
    MAS_ANDROID_WRS_CATEGORIES = {
        "mas_wrs_pinterest": [
            r"(?i)(^|\s)(pinterest|com\.pinterest)(\s|$)"
        ],
        "mas_wrs_duolingo": [
            r"(?i)(^|\s)(duolingo|com\.duolingo)(\s|$)"
        ],
        "mas_wrs_wikipedia": [
            r"(?i)(^|\s)(wikipedia|org\.wikipedia)(\s|$)"
        ],
        "mas_wrs_virtualpiano": [
            r"(?i)(virtual\s*piano)"
        ],
        "mas_wrs_youtube": [
            r"(?i)(^|\s)(youtube|com\.google\.android\.youtube)(\s|$)"
        ],
        "mas_wrs_r34m": [
            r"(?i)(((r34|rule\s?34).*monika)|(monika.*(r34|rule\s?34)))"
        ],
        "mas_wrs_monikamoddev": [
            r"(?i)monikamoddev"
        ],
        "mas_wrs_twitter": [
            r"(?i)(^|\s)(twitter|x|com\.twitter\.android)(\s|$)"
        ],
        "mas_wrs_monikatwitter": [
            r"(?i)(lilmonix3|monika\s*after\s*story)"
        ],
        "mas_wrs_4chan": [
            r"(?i)(^|\s)(4chan)(\s|$)"
        ],
        "mas_wrs_pixiv": [
            r"(?i)(^|\s)(pixiv|jp\.pixiv\.android)(\s|$)"
        ],
        "mas_wrs_reddit": [
            r"(?i)(^|\s)(reddit|com\.reddit\.frontpage)(\s|$)"
        ],
        "mas_wrs_mal": [
            r"(?i)(myanimelist|my\s*anime\s*list)"
        ],
        "mas_wrs_deviantart": [
            r"(?i)(deviantart|com\.deviantart)"
        ],
        "mas_wrs_netflix": [
            r"(?i)(^|\s)(netflix|com\.netflix\.mediaclient)(\s|$)"
        ],
        "mas_wrs_twitch": [
            r"(?i)(^|\s)(twitch|tv\.twitch\.android\.app)(\s|$)"
        ],
        "mas_wrs_word_processor": [
            r"(?i)(google\s*docs|com\.google\.android\.apps\.docs|microsoft\s*word|com\.microsoft\.office\.word|wps\s*office|cn\.wps\.moffice|libreoffice)"
        ],
        "mas_wrs_crunchyroll": [
            r"(?i)(^|\s)(crunchyroll|com\.crunchyroll\.crunchyroid)(\s|$)"
        ],
        "mas_wrs_bilibili": [
            r"(?i)(bilibili|哔哩哔哩|tv\.danmaku\.bili|com\.bilibili)"
        ],
        "mas_wrs_monikacloud": [
            r"(?i)monika\s*cloud"
        ],
    }

    def mas_update_android_wrs_categories():
        """
        Updates WRS categories to Android app-label/package-name regexes.

        OUT:
            list of updated event labels
        """
        updated_labels = []

        for ev_label, android_category in MAS_ANDROID_WRS_CATEGORIES.items():
            ev = store.mas_windowreacts.windowreact_db.get(ev_label, None)
            if ev is not None:
                ev.category = list(android_category)
                updated_labels.append(ev_label)

            persistent_ev = persistent._mas_windowreacts_database.get(ev_label, None)
            if persistent_ev is not None and persistent_ev is not ev:
                persistent_ev.category = list(android_category)

        return updated_labels

    store.MAS_ANDROID_WRS_CATEGORIES = MAS_ANDROID_WRS_CATEGORIES
    store.mas_update_android_wrs_categories = mas_update_android_wrs_categories

    if renpy.android:
        store.mas_android_wrs_categories_updated = mas_update_android_wrs_categories()
