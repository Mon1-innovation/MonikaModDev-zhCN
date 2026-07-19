init -5 python:
    """
    Dependency Check: Pyjnius
    """
    try:
        from jnius import autoclass, cast
        mas_android_backend_available = True
    except ImportError:
        mas_android_backend_available = False

init python:
    def _mas_android_jni_string(value):
        if value is None:
            return ""
        return renpy.substitute(value)

    # Stubs
    def mas_android_schedule_notif(title, message, delay_seconds=0, actions=None, special_category=None):
        pass

    def mas_android_cancel_all_notifs():
        pass

    def mas_android_send_test_notif(title, message):
        print("[MAS_ANDROID] WARNING: Backend not loaded/available. Test call stubbed.")

    def mas_android_schedule_valentine(delay_seconds, title, message):
        pass

    def mas_android_cancel_valentine():
        pass

    def mas_android_cancel_standard_only():
        pass

    def mas_android_cancel_type_sleep():
        pass

    def mas_android_clear_active_notifications():
        pass

    store.mas_android_schedule_notif = mas_android_schedule_notif
    store.mas_android_cancel_all_notifs = mas_android_cancel_all_notifs
    store.mas_android_cancel_standard_only = mas_android_cancel_standard_only
    store.mas_android_cancel_type_sleep = mas_android_cancel_type_sleep
    store.mas_android_send_test_notif = mas_android_send_test_notif
    store.mas_android_schedule_valentine = mas_android_schedule_valentine
    store.mas_android_cancel_valentine = mas_android_cancel_valentine
    store.mas_android_clear_active_notifications = mas_android_clear_active_notifications

    if persistent.mas_android_notif_enabled is None:
        persistent.mas_android_notif_enabled = True
    if persistent.mas_android_notif_sound is None:
        persistent.mas_android_notif_sound = True
    if persistent.mas_android_notif_vibration is None:
        persistent.mas_android_notif_vibration = True
    if persistent.mas_android_return_reminders is None:
        persistent.mas_android_return_reminders = True
    if persistent.mas_android_calendar_events is None:
        persistent.mas_android_calendar_events = True
    if persistent.mas_android_frequency_index is None:
        persistent.mas_android_frequency_index = 3
    if persistent.mas_android_frequency_index > 5:
        persistent.mas_android_frequency_index = 5
    if persistent.mas_android_frequency_index < 1:
        persistent.mas_android_frequency_index = 1

init 5 python:
    if mas_android_backend_available and renpy.android:
        
        def mas_android_schedule_notif(title, message, delay_seconds, actions=None, special_category=None):
            try:
                if isinstance(message, dict):
                    message = message.get("msg", "Te estaré esperando...")
                
                title = renpy.substitute(title)
                message = renpy.substitute(message)
                
                try: 
                    PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                except: 
                    PythonActivity = autoclass('org.renpy.android.PythonActivity')
                    
                NotificationHelper = autoclass('com.monikaafterstory.tec.es.NotificationHelper')
                
                context = PythonActivity.mActivity
                
                action1 = _mas_android_jni_string(actions[0]) if actions and len(actions) >= 1 else ""
                action2 = _mas_android_jni_string(actions[1]) if actions and len(actions) >= 2 else ""
                
                snd = True if persistent.mas_android_notif_sound is None else persistent.mas_android_notif_sound
                vib = True if persistent.mas_android_notif_vibration is None else persistent.mas_android_notif_vibration
                
                tag = "mas_notification"
                if special_category == "sleep" or special_category == "TYPE_SLEEP":
                    tag = "TYPE_SLEEP"

                # JNI Call
                NotificationHelper.scheduleExactNotification(
                    context, title, message, action1, action2, int(delay_seconds), tag, snd, vib
                )
                return True
                
            except Exception as e:
                print("[MAS_ANDROID] Error scheduling notification: " + str(e))
                return False

        def mas_android_schedule_valentine(delay_seconds, title, message):
            try:
                if isinstance(message, dict):
                    message = message.get("msg", "Feliz San Valentin...")
                
                title = renpy.substitute(title)
                message = renpy.substitute(message)
                
                try: 
                    PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                except: 
                    PythonActivity = autoclass('org.renpy.android.PythonActivity')
                    
                NotificationHelper = autoclass('com.monikaafterstory.tec.es.NotificationHelper')
                context = PythonActivity.mActivity
                
                NotificationHelper.scheduleExactNotification(
                    context, title, message, "", "", int(delay_seconds), "EVENT_VALENTINE", True, True
                )
                return True
                
            except Exception as e:
                print("[MAS_ANDROID_SNIPER] Error: " + str(e))
                return False

        def mas_android_cancel_all_notifs():
            try:
                try: 
                    PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                except: 
                    PythonActivity = autoclass('org.renpy.android.PythonActivity')
                    
                WorkManager = autoclass('androidx.work.WorkManager')
                context = PythonActivity.mActivity
                wm = WorkManager.getInstance(context)
                
                # We cancel by unique work names and tags that could be pending
                wm.cancelAllWorkByTag("mas_notification")
                wm.cancelAllWorkByTag("TYPE_SLEEP")
                wm.cancelUniqueWork("mas_notification_job")
                wm.cancelUniqueWork("mas_notification_job_expedited")
                
                # Also cancel ExactAlarm if pending
                AlarmManager = autoclass('android.app.AlarmManager')
                Intent = autoclass('android.content.Intent')
                PendingIntent = autoclass('android.app.PendingIntent')
                ExactAlarmReceiver = autoclass('com.monikaafterstory.tec.es.ExactAlarmReceiver')
                Context = autoclass('android.content.Context')
                
                intent = Intent(context, ExactAlarmReceiver)
                intent.setAction("com.monikaafterstory.tec.es.ACTION_TRIGGER_NOTIF")
                
                # Tags: mas_notification.hashCode(), TYPE_SLEEP.hashCode()
                String = autoclass('java.lang.String')
                tags = [String("mas_notification"), String("TYPE_SLEEP")]
                
                am = cast(AlarmManager, context.getSystemService(Context.ALARM_SERVICE))
                for t in tags:
                    pi = PendingIntent.getBroadcast(context, t.hashCode(), intent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE)
                    am.cancel(pi)
                    
            except Exception as e:
                print("[MAS_ANDROID] Cancel Error: " + str(e))

        def mas_android_cancel_valentine():
            try:
                try: 
                    PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                except: 
                    PythonActivity = autoclass('org.renpy.android.PythonActivity')

                WorkManager = autoclass('androidx.work.WorkManager')
                context = PythonActivity.mActivity
                wm = WorkManager.getInstance(context)
                
                wm.cancelAllWorkByTag("EVENT_VALENTINE")
                
                AlarmManager = autoclass('android.app.AlarmManager')
                Intent = autoclass('android.content.Intent')
                PendingIntent = autoclass('android.app.PendingIntent')
                ExactAlarmReceiver = autoclass('com.monikaafterstory.tec.es.ExactAlarmReceiver')
                
                intent = Intent(context, ExactAlarmReceiver)
                intent.setAction("com.monikaafterstory.tec.es.ACTION_TRIGGER_NOTIF")
                String = autoclass('java.lang.String')
                pi = PendingIntent.getBroadcast(context, String("EVENT_VALENTINE").hashCode(), intent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE)
                
                Context = autoclass('android.content.Context')
                am = cast(AlarmManager, context.getSystemService(Context.ALARM_SERVICE))
                am.cancel(pi)
                
            except Exception as e:
                print("[MAS_ANDROID_SNIPER] Cancel Error: " + str(e))

        def mas_android_cancel_standard_only():
            try:
                try: 
                    PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                except: 
                    PythonActivity = autoclass('org.renpy.android.PythonActivity')
                    
                WorkManager = autoclass('androidx.work.WorkManager')
                context = PythonActivity.mActivity
                wm = WorkManager.getInstance(context)
                
                wm.cancelAllWorkByTag("mas_notification")
            except:
                pass

        def mas_android_cancel_type_sleep():
            try:
                try: 
                    PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                except: 
                    PythonActivity = autoclass('org.renpy.android.PythonActivity')
                    
                WorkManager = autoclass('androidx.work.WorkManager')
                context = PythonActivity.mActivity
                wm = WorkManager.getInstance(context)
                
                wm.cancelAllWorkByTag("TYPE_SLEEP")
            except:
                pass


        def mas_android_clear_active_notifications():
            try:
                try: 
                    PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                except: 
                    PythonActivity = autoclass('org.renpy.android.PythonActivity')
                
                Context = autoclass('android.content.Context')
                NotificationManager = autoclass('android.app.NotificationManager')
                
                context = PythonActivity.mActivity
                nm = cast(NotificationManager, context.getSystemService(Context.NOTIFICATION_SERVICE))
                
                if "mas_android_cancel_all_notifs" in globals():
                    mas_android_cancel_all_notifs()
                
                nm.cancelAll()
            except Exception as e:
                print("[MAS_ANDROID] Clear Error: " + str(e))


        def mas_android_display_notif(title, message):
            try:
                title = renpy.substitute(title)
                message = renpy.substitute(message)
                
                try: 
                    PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
                except: 
                    PythonActivity = autoclass('org.renpy.android.PythonActivity')
                
                NotificationHelper = autoclass('com.monikaafterstory.tec.es.NotificationHelper')
                
                context = PythonActivity.mActivity
                
                snd = True if persistent.mas_android_notif_sound is None else persistent.mas_android_notif_sound
                vib = True if persistent.mas_android_notif_vibration is None else persistent.mas_android_notif_vibration
                
                NotificationHelper.showNotification(
                    context,
                    888, 
                    title,
                    message,
                    "", 
                    "", 
                    2,    
                    snd,  
                    vib,  
                    9000  
                )
                return True
                
            except Exception as e:
                print("[MAS_ANDROID] Display Notif Error: " + str(e))
                return False

        def mas_android_send_test_notif(title="[m_name]", message="Android notification test."):
            return mas_android_display_notif(title, message)

        store.mas_android_schedule_notif = mas_android_schedule_notif
        store.mas_android_cancel_all_notifs = mas_android_cancel_all_notifs
        store.mas_android_display_notif = mas_android_display_notif
        store.mas_android_send_test_notif = mas_android_send_test_notif
        store.mas_android_cancel_standard_only = mas_android_cancel_standard_only
        store.mas_android_cancel_type_sleep = mas_android_cancel_type_sleep
        store.mas_android_schedule_valentine = mas_android_schedule_valentine
        store.mas_android_cancel_valentine = mas_android_cancel_valentine
        store.mas_android_clear_active_notifications = mas_android_clear_active_notifications

    else:
        def mas_android_schedule_notif(title, message, delay_seconds, actions=None, special_category=None):
            print("[MAS_ANDROID] (Simulated) Scheduled in {}s: [{}] {}".format(delay_seconds, title, message))
            if actions:
                print("[MAS_ANDROID] (Simulated) With Actions: " + str(actions))
        
        def mas_android_cancel_all_notifs():
            print("[MAS_ANDROID] (Simulated) All cancelled")
            
        def mas_android_display_notif(title, message):
            print("[MAS_ANDROID] (Simulated) DISPLAY: [{}] {}".format(title, message))

        def mas_android_send_test_notif(title="[m_name]", message="Android notification test."):
            return mas_android_display_notif(title, message)
             
        store.mas_android_schedule_notif = mas_android_schedule_notif
        store.mas_android_cancel_all_notifs = mas_android_cancel_all_notifs
        store.mas_android_display_notif = mas_android_display_notif
        store.mas_android_send_test_notif = mas_android_send_test_notif
        store.mas_android_cancel_standard_only = mas_android_cancel_all_notifs
        store.mas_android_cancel_type_sleep = mas_android_cancel_all_notifs
        store.mas_android_clear_active_notifications = mas_android_cancel_all_notifs
