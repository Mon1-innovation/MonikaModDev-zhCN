#NOTE: This ONLY works for Windows atm

#Whether Monika can use notifications or not
default persistent._mas_enable_notifications = False

#Whether notification sounds are enabled or not
default persistent._mas_notification_sounds = True

#Whether Monika can see your active window or not
default persistent._mas_windowreacts_windowreacts_enabled = False

#Persistent windowreacts db
default persistent._mas_windowreacts_database = dict()

#A global list of events we DO NOT want to unlock on a new session
default persistent._mas_windowreacts_no_unlock_list = list()

#A dict of locations where notifs are used, and if they're enabled for said location
default persistent._mas_windowreacts_notif_filters = dict()

init -10 python in mas_windowreacts:
    #We need this in case we cannot get access to the libs, so everything can still run
    can_show_notifs = True

    #If we don't have access to the required libs to do windowreact related things
    can_do_windowreacts = True

    #The windowreacts db
    windowreact_db = {}

    #Group list, to populate the menu screen
    #NOTE: We do this so that we don't have to try to get a notification
    #In order for it to show up in the menu and in the dict
    _groups_list = [
        "Topic Alerts",
        "Window Reactions",
    ]

init python in mas_windowutils:
    import os

    import store
    from store import mas_utils
    #The initial setup

    ## Linux
    # The window object, used on Linux systems, otherwise always None
    MAS_WINDOW = None

    ## Windows
    # The notification manager
    WIN_NOTIF_MANAGER = None
    # Window handler
    HWND = None

    #We can only do this on windows
    if renpy.windows:
        #We need to extend the sys path to see our packages
        import sys
        sys.path.append(renpy.config.gamedir + '\\python-packages\\')

        #We try/catch/except to make sure the game can run if load fails here
        try:
            import winnie32api

            #Now we initialize the notification class
            WIN_NOTIF_MANAGER = winnie32api.NotifManager(
                renpy.config.name,
                os.path.join(renpy.config.gamedir, "mod_assets/mas_icon.ico"),
                on_dismiss=lambda: (
                    focusMASWindow(),
                    _unflashMASWindow_Windows(),
                    WIN_NOTIF_MANAGER.clear()
                ),
                on_lmb_click=lambda: (
                    focusMASWindow(),
                    _unflashMASWindow_Windows(),
                    WIN_NOTIF_MANAGER.clear()
                ),
                on_rmb_click=lambda: (
                    _unflashMASWindow_Windows(),
                    WIN_NOTIF_MANAGER.clear()
                )
            )

        except Exception as e:
            #If we fail to import, then we're going to have to make sure nothing can run.
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False

            #Log this
            store.mas_utils.mas_log.warning(
                f"winnie32api failed to be imported, disabling notifications: {e}"
            )

    elif renpy.linux:
        #Get session type
        session_type = os.environ.get("XDG_SESSION_TYPE")

        #Wayland is not supported, disable wrs
        if session_type in ("wayland", None) or os.environ.get("WAYLAND_DISPLAY"):
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False
            store.mas_utils.mas_log.warning("Wayland is not yet supported, disabling notifications.")

        #X11 however is fine
        elif session_type == "x11" or os.environ.get("DISPLAY"):
            try:
                import Xlib

                from Xlib.display import Display
                from Xlib.error import BadWindow, XError

                __display = Display()
                __root = __display.screen().root

            except Exception as e:
                store.mas_windowreacts.can_show_notifs = False
                store.mas_windowreacts.can_do_windowreacts = False

                store.mas_utils.mas_log.warning(
                    f"Xlib failed to be imported, disabling notifications: {e}"
                )

        else:
            store.mas_windowreacts.can_show_notifs = False
            store.mas_windowreacts.can_do_windowreacts = False

            store.mas_utils.mas_log.warning("Cannot detect current session type, disabling notifications.")

    else:
        store.mas_windowreacts.can_do_windowreacts = False


    #Fallback Const Defintion
    DEF_MOUSE_POS_RETURN = (0, 0)


    ##Now, we start defining OS specific functions which we can set to a var for proper cross platform on a single func
    #Firstly, the internal helper functions
    def __getActiveWindow_Linux():
        """
        Gets the active window object

        OUT:
            Xlib.display.Window, or None if errors occur (or not possible to get window obj)
        """
        #If not possible to get active window, we'll just return None
        if not store.mas_windowreacts.can_do_windowreacts:
            return None

        NET_ACTIVE_WINDOW = __display.intern_atom("_NET_ACTIVE_WINDOW")

        # Perform nullchecks on property getters, just in case.
        active_winid_prop = __root.get_full_property(NET_ACTIVE_WINDOW, 0)

        if active_winid_prop is None:
            return None

        active_winid = active_winid_prop.value[0]

        try:
            return __display.create_resource_object("window", active_winid)
        except XError as e:
            mas_utils.mas_log.error("Failed to get active window object: {}".format(e))
            return None

    def __getMASWindow_Linux():
        """
        Funtion to get the MAS window on Linux systems

        OUT:
            Xlib.display.Window representing the MAS window

        ASSUMES: OS IS LINUX (renpy.linux)
        """
        #If not possible to get MAS window, we'll just return None
        if not store.mas_windowreacts.can_do_windowreacts:
            return None

        NET_CLIENT_LIST_ATOM = __display.intern_atom('_NET_CLIENT_LIST', False)

        try:
            prop = __root.get_full_property(NET_CLIENT_LIST_ATOM, 0)
            # Apparently x-window can return None here, the reason is unknown to me,
            # but we can just sanity check it, per #9421
            if prop is None:
                return

            winid_list = prop.value
            for winid in winid_list:
                win = __display.create_resource_object("window", winid)
                transient_for = win.get_wm_transient_for()
                winname = win.get_wm_name()

                if transient_for is None and winname and store.mas_getWindowTitle() == winname:
                    return win

        except XError as e:
            mas_utils.mas_log.error("Failed to get MAS window object: {}".format(e))
            return None

    def __getMASWindowHWND_Windows() -> int|None:
        """
        Gets the hWnd of the MAS window

        OUT:
            int - represents the hWnd of the MAS window
            None - if we failed to get hwnd
        """
        global HWND

        #Verify we can actually do this before doing anything
        if store.mas_windowreacts.can_do_windowreacts:
            if HWND is None:
                try:
                    HWND = winnie32api.get_hwnd_by_title(store.mas_getWindowTitle())
                except Exception as e:
                    HWND = None
                    mas_utils.mas_log.error(f"Failed to get MAS window hwnd: {e}")
        else:
            HWND = None

        return HWND

    def __getAbsoluteGeometry_Linux(win):
        """
        Returns the (x, y, height, width) of a window relative to the top-left
        of the screen.

        IN:
            win - Xlib.display.Window object representing the window we wish to get absolute geometry of

        OUT:
            tuple, (x, y, width, height) if possible, otherwise None
        """
        #If win is None, then we should just return a None here
        if win is None:
            # This handles some odd issues with setting window on Linux
            win = _setMASWindow_Linux()
            if win is None:
                return None

        try:
            geom = win.get_geometry()
            (x, y) = (geom.x, geom.y)

            while True:
                parent = win.query_tree().parent
                pgeom = parent.get_geometry()
                x += pgeom.x
                y += pgeom.y
                if parent.id == __root.id:
                    break
                win = parent

            return (x, y, geom.width, geom.height)

        except Xlib.error.BadDrawable:
            #In the case of a bad drawable, we'll try to re-get the MAS window to get a good one
            _setMASWindow_Linux()

        except XError as e:
            mas_utils.mas_log.error(f"Failed to get window geometry: {e}")

        return None

    def _setMASWindow_Linux():
        """
        Sets the MAS_WINDOW global on Linux systems

        OUT:
            the window object
        """
        global MAS_WINDOW

        if renpy.linux:
            MAS_WINDOW = __getMASWindow_Linux()

        else:
            MAS_WINDOW = None

        return MAS_WINDOW

    #Next, the active window handle getters
    def _getActiveWindowHandle_Windows() -> str:
        """
        Funtion to get the active window on Windows systems

        OUT:
            string representing the active window handle

        ASSUMES: OS IS WINDOWS (renpy.windows)
        """
        try:
            # winnie32api can return None
            return winnie32api.get_active_window_title() or ""
        except Exception:
            return ""

    def _getActiveWindowHandle_Linux() -> str:
        """
        Funtion to get the active window on Linux systems

        OUT:
            string representing the active window handle

        ASSUMES: OS IS LINUX (renpy.linux)
        """
        NET_WM_NAME = __display.intern_atom("_NET_WM_NAME")
        active_winobj = __getActiveWindow_Linux()

        if active_winobj is None:
            return ""

        try:
            # Subsequent method calls might raise BadWindow exception if active_winid refers to nonexistent window.
            active_winname_prop = active_winobj.get_full_property(NET_WM_NAME, 0)

            # TODO: consider logging if this is None, also catch a more generic exception just in case
            if active_winname_prop is not None:
                active_winname = unicode(active_winname_prop.value, encoding = "utf-8")
                return active_winname.replace("\n", "")

        except (XError, BadWindow) as e:
            mas_utils.mas_log.error(f"Failed to get active window handle: {e}")

        return ""

    def _getActiveWindowHandle_OSX() -> str:
        """
        Gets the active window on macOS

        NOTE: This currently just returns an empty string, this is because we do not have active window detection
        for MacOS
        """
        return ""

    def _flashMASWindow_Windows():
        """
        Tries to flash MAS window
        """
        hwnd = __getMASWindowHWND_Windows()
        if hwnd:
            winnie32api.flash_window(
                hwnd,
                count=None,
                caption=False,
                tray=True
            )

    def _unflashMASWindow_Windows():
        """
        Tries to stop flashing MAS window
        """
        hwnd = __getMASWindowHWND_Windows()
        if hwnd:
            winnie32api.unflash_window(hwnd)

    def _flashMASWindow_Linux():
        """
        Tries to flash MAS window
        """

    def _flashMASWindow_OSX():
        """
        Tries to flash MAS window
        """

    def _focusMASWindow_Windows():
        """
        Tries to set focus on MAS window
        """
        hwnd = __getMASWindowHWND_Windows()
        if hwnd:
            winnie32api.set_active_window(hwnd)

    def _focusMASWindow_Linux():
        """
        Tries to set focus on MAS window
        """

    def _focusMASWindow_OSX():
        """
        Tries to set focus on MAS window
        """

    #Notif show internals
    def _tryShowNotification_Windows(title, body):
        """
        Tries to push a notification to the notification center on Windows.
        If it can't it should fail silently to the user.

        IN:
            title - notification title
            body - notification body

        OUT:
            bool. True if the notification was successfully sent, False otherwise
        """
        try:
            return WIN_NOTIF_MANAGER.send(title, body)
        except Exception:
            return False

    def _tryShowNotification_Linux(title, body):
        """
        Tries to push a notification to the notification center on Linux.
        If it can't it should fail silently to the user.

        IN:
            title - notification title
            body - notification body

        OUT:
            bool - True, representing the notification's success
        """
        # Single quotes have to be escaped.
        # Since single quoting in POSIX shell doesn't allow escaping,
        # we have to close the quotation, insert a literal single quote and reopen the quotation.
        body  = body.replace("'", "'\\''")
        title = title.replace("'", "'\\''") # better safe than sorry
        os.system("notify-send '{0}' '{1}' -a 'Monika' -u low".format(title, body))
        return True

    def _tryShowNotification_OSX(title, body):
        """
        Tries to push a notification to the notification center on macOS.
        If it can't it should fail silently to the user.

        IN:
            title - notification title
            body - notification body

        OUT:
            bool - True, representing the notification's success
        """
        os.system('osascript -e \'display notification "{0}" with title "{1}"\''.format(body, title))
        return True

    #Mouse Position related funcs
    def _getAbsoluteMousePos_Windows():
        """
        Returns an (x, y) co-ord tuple for the mouse position

        OUT:
            tuple representing the absolute position of the mouse
        """
        if store.mas_windowreacts.can_do_windowreacts:
            #Try except here because we may not have permissions to do so
            try:
                cur_pos = tuple(winnie32api.get_screen_mouse_pos())

            except Exception:
                cur_pos = DEF_MOUSE_POS_RETURN

        else:
            cur_pos = DEF_MOUSE_POS_RETURN

        return cur_pos

    def _getAbsoluteMousePos_Linux():
        """
        Returns an (x, y) co-ord tuple represening the absolute mouse position
        """
        mouse_data = __root.query_pointer()._data
        return (mouse_data["root_x"], mouse_data["root_y"])

    #Window position related
    def _getMASWindowPos_Windows():
        """
        Gets the window position for MAS as a tuple of (left, top, right, bottom)

        OUT:
            tuple representing window geometry or None if the window's hWnd could not be found
        """
        hwnd = __getMASWindowHWND_Windows()

        if hwnd is None:
            return None

        try:
            rect = winnie32api.get_window_rect(hwnd)
        except Exception:
            return None

        # Windows may return incorrect geometry (-32k seems to be the limit),
        # in this case we return None
        if rect.top_left.x <= -32000 and rect.top_left.y <= -32000:
            return None

        return (rect.top_left.x, rect.top_left.y, rect.bottom_right.x, rect.bottom_right.y)

    def _getMASWindowPos_Linux():
        """
        Returns (x1, y1, x2, y2) relative to the top-left of the screen.

        OUT:
            tuple representing (left, top, right, bottom) of the window bounds, or None if not possible to get
        """
        geom = __getAbsoluteGeometry_Linux(MAS_WINDOW)

        if geom is not None:
            return (
                geom[0],
                geom[1],
                geom[0] + geom[2],
                geom[1] + geom[3]
            )
        return None

    def getMousePosRelative():
        """
        Gets the mouse position relative to the MAS window.
        Returned as a set of coordinates (0, 0) being within the MAS window, (1, 0) being to the left, (0, 1) being above, etc.

        OUT:
            Tuple representing the location of the mouse relative to the MAS window in terms of coordinates
        """
        pos_tuple = getMASWindowPos()

        if pos_tuple is None:
            return (0, 0)

        left, top, right, bottom = pos_tuple

        mouse_x, mouse_y = getMousePos()
        # NOTE: This is so we get correct pos in fullscreen
        if mouse_x == 0:
            mouse_x = 1
        if mouse_y == 0:
            mouse_y = 1

        half_mas_window_width = (right - left)/2
        half_mas_window_height = (bottom - top)/2

        # Sanity check since we'll divide by these,
        # Can be zeros in some rare cases: #9088
        if half_mas_window_width == 0 or half_mas_window_height == 0:
            return (0, 0)

        mid_mas_window_x = left + half_mas_window_width
        mid_mas_window_y = top + half_mas_window_height

        mas_window_to_cursor_x_comp = mouse_x - mid_mas_window_x
        mas_window_to_cursor_y_comp = mouse_y - mid_mas_window_y

        #Divide to handle the middle case
        mas_window_to_cursor_x_comp = int(float(mas_window_to_cursor_x_comp)/half_mas_window_width)
        mas_window_to_cursor_y_comp = -int(float(mas_window_to_cursor_y_comp)/half_mas_window_height)

        #Now return the unit vector direction
        return (
            mas_window_to_cursor_x_comp/abs(mas_window_to_cursor_x_comp) if mas_window_to_cursor_x_comp else 0,
            mas_window_to_cursor_y_comp/abs(mas_window_to_cursor_y_comp) if mas_window_to_cursor_y_comp else 0
        )

    def isCursorInMASWindow():
        """
        Checks if the cursor is within the MAS window

        OUT:
            True if cursor is within the mas window (within x/y), False otherwise
            Also returns True if we cannot get window position
        """
        return getMousePosRelative() == (0, 0)

    def isCursorLeftOfMASWindow():
        """
        Checks if the cursor is to the left of the MAS window (must be explicitly to the left of the left window bound)

        OUT:
            True if cursor is to the left of the window, False otherwise
            Also returns False if we cannot get window position
        """
        return getMousePosRelative()[0] == -1

    def isCursorRightOfMASWindow():
        """
        Checks if the cursor is to the right of the MAS window (must be explicitly to the right of the right window bound)

        OUT:
            True if cursor is to the right of the window, False otherwise
            Also returns False if we cannot get window position
        """
        return getMousePosRelative()[0] == 1

    def isCursorAboveMASWindow():
        """
        Checks if the cursor is above the MAS window (must be explicitly above the window bound)

        OUT:
            True if cursor is above the window, False otherwise
            False as well if we're unable to get a window position
        """
        return getMousePosRelative()[1] == 1

    def isCursorBelowMASWindow():
        """
        Checks if the cursor is above the MAS window (must be explicitly above the window bound)

        OUT:
            True if cursor is above the window, False otherwise
            False as well if we're unable to get a window position
        """
        return getMousePosRelative()[1] == -1

    #Fallback functions because Mac
    def return_true():
        """
        Literally returns True
        """
        return True

    def return_false():
        """
        Literally returns False
        """
        return False

    #Finally, we set vars accordingly to use the appropriate functions without needing to run constant runtime checks
    if renpy.windows:
        _window_get = _getActiveWindowHandle_Windows
        _tryShowNotif = _tryShowNotification_Windows
        getMASWindowPos = _getMASWindowPos_Windows
        getMousePos = _getAbsoluteMousePos_Windows
        flashMASWindow = _flashMASWindow_Windows
        focusMASWindow = _focusMASWindow_Windows

    elif renpy.linux:
        _window_get = _getActiveWindowHandle_Linux
        _tryShowNotif = _tryShowNotification_Linux
        getMASWindowPos = _getMASWindowPos_Linux
        getMousePos = _getAbsoluteMousePos_Linux
        flashMASWindow = _flashMASWindow_Linux
        focusMASWindow = _focusMASWindow_Linux

    else:
        _window_get = _getActiveWindowHandle_OSX
        _tryShowNotif = _tryShowNotification_OSX
        flashMASWindow = _flashMASWindow_OSX
        focusMASWindow = _focusMASWindow_OSX

        #Because we have no method of testing on Mac, we'll use the dummy function for these
        getMASWindowPos = store.dummy
        getMousePos = store.dummy

        #Now make sure we don't use these functions so long as we can't validate Mac
        # isCursorAboveMASWindow = return_false
        # isCursorBelowMASWindow = return_false
        # isCursorLeftOfMASWindow = return_false
        # isCursorRightOfMASWindow = return_false
        # isCursorInMASWindow = return_true

init python:
    #List of notif quips (used for topic alerts)
    #Windows/Linux
    mas_win_notif_quips = [
        "[player], I want to talk to you about something.",
        "Are you there, [player]?",
        "Can you come here for a second?",
        "[player], do you have a second?",
        "I have something to tell you, [player]!",
        "Do you have a minute, [player]?",
        "I've got something to talk about, [player]!",
    ]

    #OSX, since no active window detection
    mas_other_notif_quips = [
        "I've got something to talk about, [player]!",
        "I have something to tell you, [player]!",
        "Hey [player], I want to tell you something.",
        "Do you have a minute, [player]?",
    ]


    #START: Utility methods
    def mas_canCheckActiveWindow():
        """
        Checks if we can check the active window (simplifies conditionals)
        """
        return (
            store.mas_windowreacts.can_do_windowreacts
            and (persistent._mas_windowreacts_windowreacts_enabled or persistent._mas_enable_notifications)
        )

    def mas_getActiveWindowHandle():
        """
        Gets the active window name

        OUT:
            The active window handle if found. If it is not possible to get, we return an empty string

        NOTE: THIS SHOULD NEVER RETURN NONE
        """
        if mas_windowreacts.can_show_notifs and mas_canCheckActiveWindow():
            return store.mas_windowutils._window_get()
        return ""

    def mas_display_notif(
        title: str,
        body: list[str],
        group: str|None = None,
        skip_checks: bool = False,
        flash_window: bool = False
    ) -> bool:
        """
        Notification creation method

        IN:
            title - Notification heading text
            body - A list of items which would go in the notif body (one is picked at random)
            group - Notification group (for checking if we have this enabled)
                (Default: None)
            skip_checks - Whether or not we skips checks
                (Default: False)
            flash_window - do we want to flash the MAS window (tray icon)

        OUT:
            bool indicating status (notif shown or not (by check))

        NOTE:
            We only show notifications if:
                1. We are able to show notifs
                2. MAS isn't the active window
                3. User allows them
                4. And if the notification group is enabled
                OR if we skip checks. BUT this should only be used for introductory or testing purposes.
        """
        #First we want to create this location in the dict, but don't add an extra location if we're skipping checks
        if persistent._mas_windowreacts_notif_filters.get(group) is None and not skip_checks:
            persistent._mas_windowreacts_notif_filters[group] = False

        notif_success = False

        if (
            skip_checks
            or (
                mas_windowreacts.can_show_notifs
                and ((renpy.windows and not mas_isFocused()) or not renpy.windows)
                and mas_notifsEnabledForGroup(group)
            )
        ):
            #Now we make the notif
            notif_success = mas_windowutils._tryShowNotif(
                renpy.substitute(title),
                renpy.substitute(renpy.random.choice(body))
            )
            if notif_success:
                # Flash the window if needed
                if flash_window:
                    mas_windowutils.flashMASWindow()

                #Play the notif sound if we have that enabled and notif was successful
                if persistent._mas_notification_sounds:
                    renpy.sound.play("mod_assets/sounds/effects/notif.wav")

        #Now we return true if notif was successful, false otherwise
        return notif_success

    def mas_isFocused():
        """
        Checks if MAS is the focused window
        """
        #TODO: Mac vers (if possible)
        return store.mas_windowreacts.can_show_notifs and mas_getActiveWindowHandle() == store.mas_getWindowTitle()

    def mas_isInActiveWindow(regexp, active_window_handle=None):
        """
        Checks if ALL keywords are in the active window name
        IN:
            regexp:
                Regex pattern to identify the window

            active_window_handle:
                String representing the handle of the active window
                If None, it's fetched
                (Default: None)
        """

        #Don't do work if we don't have to
        if not store.mas_windowreacts.can_show_notifs:
            return False

        #Otherwise, let's get the active window
        if active_window_handle is None:
            active_window_handle = mas_getActiveWindowHandle()

        return bool(re.findall(regexp, active_window_handle))

    def mas_clearNotifs():
        """
        Clears all tray icons (also action center on win10)
        """
        if renpy.windows:
            mas_windowutils.WIN_NOTIF_MANAGER.clear()

    def mas_checkForWindowReacts():
        """
        Runs through events in the windowreact_db to see if we have a reaction, and if so, queue it
        """
        #Do not check anything if we're not supposed to
        if not persistent._mas_windowreacts_windowreacts_enabled or not store.mas_windowreacts.can_show_notifs:
            return

        active_window_handle = mas_getActiveWindowHandle()
        for ev_label, ev in mas_windowreacts.windowreact_db.items():
            if (
                Event._filterEvent(ev, unlocked=True, aff=store.mas_curr_affection)
                and ev.checkConditional()
                and mas_isInActiveWindow(ev.category[0], active_window_handle)
                and ((not store.mas_globals.in_idle_mode) or (store.mas_globals.in_idle_mode and ev.show_in_idle))
                and mas_notifsEnabledForGroup(ev.rules.get("notif-group"))
            ):
                MASEventList.queue(ev_label)
                ev.unlocked = False

                #Add the blacklist
                if "no_unlock" in ev.rules:
                    mas_addBlacklistReact(ev_label)

    def mas_resetWindowReacts(excluded=persistent._mas_windowreacts_no_unlock_list):
        """
        Runs through events in the windowreact_db to unlock them
        IN:
            List of ev_labels to exclude from being unlocked
        """
        for ev_label, ev in mas_windowreacts.windowreact_db.items():
            if ev_label not in excluded:
                ev.unlocked=True

    def mas_updateFilterDict():
        """
        Updates the filter dict with the groups in the groups list for the settings menu
        """
        for group in store.mas_windowreacts._groups_list:
            if persistent._mas_windowreacts_notif_filters.get(group) is None:
                persistent._mas_windowreacts_notif_filters[group] = False

    def mas_addBlacklistReact(ev_label):
        """
        Adds the given ev_label to the no unlock list
        IN:
            ev_label: eventlabel to add to the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label not in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.append(ev_label)

    def mas_removeBlacklistReact(ev_label):
        """
        Removes the given ev_label to the no unlock list if exists
        IN:
            ev_label: eventlabel to remove from the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.remove(ev_label)

    def mas_notifsEnabledForGroup(group):
        """
        Checks if notifications are enabled, and if enabled for the specified group
        IN:
            group: notification group to check
        """
        return persistent._mas_enable_notifications and persistent._mas_windowreacts_notif_filters.get(group,False)

    def mas_unlockFailedWRS(ev_label=None):
        """
        Unlocks a wrs again provided that it showed, but failed to show (failed checks in the notif label)
        NOTE: This should only be used for wrs that are only a notification
        IN:
            ev_label: eventlabel of the wrs
        """
        if (
            ev_label
            and renpy.has_label(ev_label)
            and ev_label not in persistent._mas_windowreacts_no_unlock_list
        ):
            mas_unlockEVL(ev_label,"WRS")

    def mas_prepForReload():
        """
        Handles clearing wrs notifs and unregistering the wndclass to allow 'reload' to work properly

        ASSUMES: renpy.windows
        """
        store.mas_clearNotifs()
