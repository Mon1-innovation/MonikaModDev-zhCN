package com.monikaafterstory.tec.es;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationChannelGroup;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.PorterDuff;
import android.graphics.PorterDuffXfermode;
import android.graphics.Rect;
import android.media.AudioAttributes;
import android.net.Uri;
import android.os.Build;
import android.text.Spannable;
import android.text.SpannableString;
import android.text.style.ForegroundColorSpan;
import androidx.core.app.NotificationCompat;
import androidx.core.app.Person;
import androidx.core.content.pm.ShortcutInfoCompat;
import androidx.core.content.pm.ShortcutManagerCompat;
import androidx.core.graphics.drawable.IconCompat;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;

public class NotificationHelper {

    public static final String TAG = "MAS_HELPER";
    private static final String CHANNEL_GROUP_ID = "mas_group";
    private static final String CHANNEL_GROUP_NAME = "Monika After Story";
    private static final String CHANNEL_ID_INTERACTIVE = "mas_v7";
    private static final String CHANNEL_ID_BIRTHDAY = "mas_v8";
    private static final String CHANNEL_ID_RANDOM = "mas_v9";
    private static final String CHANNEL_ID_SPECIAL = "mas_v10";
    private static final String SHORTCUT_ID = "monika_chat_shortcut";
    private static boolean legacyChannelsCleaned = false;

    public static final int NOTIFICATION_ID_STICKY = 777;
    public static final int TYPE_INGAME_EVENT = 2;
    public static final int TYPE_REMINDER = 0;
    public static final int TYPE_INTERACTIVE = 1;

    public static Notification buildNotification(Context context, String title, String message, String action1,
            String action2, int type, boolean sound, boolean vibration, String jobTag) {
        log(context, "");
        NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        String channelId = resolveChannelId(type, jobTag);

        createFinalizedChannels(context, nm, sound, vibration);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, channelId);
        int appIconId = context.getResources().getIdentifier("icon", "mipmap", context.getPackageName());
        int smallIconId = appIconId;
        if (smallIconId == 0) {
            smallIconId = context.getResources().getIdentifier("ic_stat_smoll", "drawable", context.getPackageName());
        }
        if (smallIconId == 0) {
            smallIconId = android.R.drawable.sym_def_app_icon;
        }
        int actionColor = Color.parseColor("#ffbce0");

        builder.setSmallIcon(smallIconId)
                .setColor(actionColor)
                .setPriority(NotificationCompat.PRIORITY_MAX)
                .setCategory(NotificationCompat.CATEGORY_MESSAGE)
                .setContentTitle(title)
                .setContentText(message)
                .setVisibility(NotificationCompat.VISIBILITY_PUBLIC);

        if (sound) {
            int soundId = context.getResources().getIdentifier("notif", "raw", context.getPackageName());
            if (soundId != 0) {
                Uri soundUri = Uri.parse("android.resource://" + context.getPackageName() + "/" + soundId);
                builder.setSound(soundUri);
            } else {
                builder.setDefaults(Notification.DEFAULT_SOUND);
            }
        }
        if (vibration) {
            builder.setVibrate(new long[] { 0, 250, 250, 250 });
        }

        Intent launchIntent = context.getPackageManager().getLaunchIntentForPackage(context.getPackageName());
        if (launchIntent != null) {
            launchIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP
                    | Intent.FLAG_ACTIVITY_SINGLE_TOP);
            launchIntent.putExtra("launch_from_notif", true);
        }

        if (type != TYPE_INTERACTIVE && launchIntent != null) {
            PendingIntent piBody = PendingIntent.getActivity(context, 0, launchIntent,
                    PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            builder.setContentIntent(piBody);
        }

        Bitmap originalBitmap = null;
        int monikaResId = context.getResources().getIdentifier("monika_contact_icon", "drawable", context.getPackageName());
        if (monikaResId == 0) {
            monikaResId = context.getResources().getIdentifier("notify_icon", "drawable", context.getPackageName());
        }
        if (monikaResId == 0) {
            monikaResId = context.getResources().getIdentifier("monika_profile", "drawable", context.getPackageName());
        }
        if (monikaResId == 0) {
            monikaResId = smallIconId;
        }
        originalBitmap = decodeSampledBitmapFromResource(context.getResources(), monikaResId, 256, 256);
        Bitmap circularBitmap = getCircleBitmap(originalBitmap);

        Person.Builder personBuilder = new Person.Builder()
                .setName(title)
                .setImportant(true)
                .setBot(false);
        if (circularBitmap != null) {
            personBuilder.setIcon(IconCompat.createWithBitmap(circularBitmap));
        }
        Person monikaUser = personBuilder.build();
        NotificationCompat.MessagingStyle style = new NotificationCompat.MessagingStyle(monikaUser)
                .setGroupConversation(false)
                .addMessage(message, System.currentTimeMillis(), monikaUser);

        builder.setStyle(style)
                .addPerson(monikaUser);
        builder.setShortcutId("monika_chat_shortcut");
        if (circularBitmap != null) {
            builder.setLargeIcon(circularBitmap);
        }

        registerConversationShortcut(context, monikaUser, circularBitmap, launchIntent);

        if (type == TYPE_INTERACTIVE) {
            if (action1 != null && action1.length() > 0 && launchIntent != null) {
                PendingIntent piLaunch = PendingIntent.getActivity(context, 101, launchIntent,
                        PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
                builder.addAction(0, getStyledText(action1, actionColor), piLaunch);
            }
            if (action2 != null && action2.length() > 0) {
                Intent dismissIntent = new Intent(context, NotificationActionReceiver.class);
                dismissIntent.setAction("com.monikaafterstory.tec.es.ACTION_DISMISS");
                dismissIntent.putExtra("notification_id", NOTIFICATION_ID_STICKY);
                if (jobTag != null) {
                    dismissIntent.putExtra("job_tag", jobTag);
                }
                PendingIntent piDismiss = PendingIntent.getBroadcast(context, 102, dismissIntent,
                        PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
                builder.addAction(0, getStyledText(action2, actionColor), piDismiss);
            }
            builder.setOngoing(false);
            builder.setAutoCancel(true);
            builder.setLocalOnly(true);
            builder.setOnlyAlertOnce(true);
            builder.setCategory(NotificationCompat.CATEGORY_MESSAGE);
        } else {
            builder.setAutoCancel(true);
        }

        return builder.build();
    }

    public static void showNotification(Context context, int notifId, String title, String message, String action1,
            String action2, int type, boolean sound, boolean vibration, long timeoutMs) {
        log(context, "");
        Notification n = buildNotification(context, title, message, action1, action2, type, sound, vibration, null);
        NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        if (nm != null) {
            nm.notify(notifId, n);
            if (timeoutMs > 0) {
                new android.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> {
                    try {
                        nm.cancel(notifId);
                    } catch (Exception e) {
                    }
                }, timeoutMs);
            }
        }
    }

    private static String resolveChannelId(int type, String jobTag) {
        if (type == TYPE_INTERACTIVE) {
            return CHANNEL_ID_INTERACTIVE;
        }

        String normalizedTag = jobTag == null ? "" : jobTag.toLowerCase(Locale.ROOT);
        if (normalizedTag.contains("birthday") || normalizedTag.contains("cumple")) {
            return CHANNEL_ID_BIRTHDAY;
        }
        if (type == TYPE_INGAME_EVENT || normalizedTag.startsWith("event_") || normalizedTag.startsWith("type_")) {
            return CHANNEL_ID_SPECIAL;
        }

        return CHANNEL_ID_RANDOM;
    }

    private static void createFinalizedChannels(Context context, NotificationManager nm, boolean sound,
            boolean vibration) {
        if (nm == null || Build.VERSION.SDK_INT < Build.VERSION_CODES.O) {
            return;
        }

        cleanupLegacyChannels(nm);

        NotificationChannelGroup group = new NotificationChannelGroup(CHANNEL_GROUP_ID, CHANNEL_GROUP_NAME);
        nm.createNotificationChannelGroup(group);

        createChannel(context, nm, CHANNEL_ID_INTERACTIVE, text("Interactive Actions", "Acciones interactivas"),
                text("Farewells and notifications with buttons.", "Despedidas y notificaciones con botones."),
                sound, vibration);
        createChannel(context, nm, CHANNEL_ID_BIRTHDAY, text("Birthdays", "Cumpleanos"),
                text("Birthday reminders and messages.", "Recordatorios y mensajes de cumpleanos."),
                sound, vibration);
        createChannel(context, nm, CHANNEL_ID_RANDOM, text("Random Greetings", "Saludos aleatorios"),
                text("Default Monika greetings and return reminders.",
                        "Saludos predeterminados de Monika y recordatorios de regreso."),
                sound, vibration);
        createChannel(context, nm, CHANNEL_ID_SPECIAL, text("Special Events", "Eventos especiales"),
                text("Calendar events and special reminders.", "Eventos del calendario y recordatorios especiales."),
                sound, vibration);
    }

    private static void createChannel(Context context, NotificationManager nm, String channelId, String name,
            String description, boolean sound, boolean vibration) {
        if (nm.getNotificationChannel(channelId) != null) {
            return;
        }

        NotificationChannel chan = new NotificationChannel(channelId, name, NotificationManager.IMPORTANCE_HIGH);
        chan.setDescription(description);
        chan.setGroup(CHANNEL_GROUP_ID);
        chan.setLockscreenVisibility(NotificationCompat.VISIBILITY_PUBLIC);
        if (sound) {
            int soundId = context.getResources().getIdentifier("notif", "raw", context.getPackageName());
            Uri soundUri = (soundId != 0)
                    ? Uri.parse("android.resource://" + context.getPackageName() + "/" + soundId)
                    : null;
            AudioAttributes audioAttributes = new AudioAttributes.Builder()
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                    .setUsage(AudioAttributes.USAGE_NOTIFICATION)
                    .build();
            if (soundUri != null) {
                chan.setSound(soundUri, audioAttributes);
            }
        } else {
            chan.setSound(null, null);
        }
        chan.enableVibration(vibration);
        if (vibration) {
            chan.setVibrationPattern(new long[] { 0, 250, 250, 250 });
        }
        chan.enableLights(true);
        nm.createNotificationChannel(chan);
    }

    private static synchronized void cleanupLegacyChannels(NotificationManager nm) {
        if (legacyChannelsCleaned || Build.VERSION.SDK_INT < Build.VERSION_CODES.O) {
            return;
        }

        for (int version = 1; version <= 6; version++) {
            deleteLegacyChannel(nm, "mas_v" + version);
            deleteLegacyChannel(nm, "mas_android_channel_v" + version);
            deleteLegacyChannel(nm, "mas_android_channel_v" + version + "_sticky_foreground");

            for (int sound = 0; sound <= 1; sound++) {
                for (int vibration = 0; vibration <= 1; vibration++) {
                    String suffix = "_s" + sound + "v" + vibration;
                    deleteLegacyChannel(nm, "mas_android_channel_v" + version + suffix);
                    deleteLegacyChannel(nm, "mas_android_channel_v" + version + "_sticky_foreground" + suffix);
                }
            }
        }

        legacyChannelsCleaned = true;
    }

    private static void deleteLegacyChannel(NotificationManager nm, String channelId) {
        try {
            nm.deleteNotificationChannel(channelId);
        } catch (Exception e) {
        }
    }

    private static String text(String english, String spanish) {
        String language = Locale.getDefault().getLanguage();
        return "es".equals(language) ? spanish : english;
    }

    private static void registerConversationShortcut(Context context, Person monikaUser, Bitmap circularBitmap,
            Intent launchIntent) {
        try {
            if (launchIntent == null) {
                return;
            }

            Set<String> categories = new HashSet<String>();
            categories.add("android.shortcut.conversation");

            ShortcutInfoCompat.Builder shortcutBuilder = new ShortcutInfoCompat.Builder(context, SHORTCUT_ID)
                    .setShortLabel("Monika")
                    .setLongLabel("Monika After Story")
                    .setPerson(monikaUser)
                    .setCategories(categories)
                    .setIntent(launchIntent)
                    .setLongLived(true);

            if (circularBitmap != null) {
                shortcutBuilder.setIcon(IconCompat.createWithBitmap(circularBitmap));
            }

            ShortcutInfoCompat shortcut = shortcutBuilder.build();
            ShortcutManagerCompat.pushDynamicShortcut(context, shortcut);
        } catch (Exception e) {
            TelemetryLogger.logError(context, "NotificationHelper", "Failed to register conversation shortcut", e,
                    TelemetryLogger.CODE_500);
        }
    }

    private static Bitmap getCircleBitmap(Bitmap bitmap) {
        if (bitmap == null) {
            return null;
        }
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();
        Bitmap output = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(output);
        final Paint paint = new Paint();
        final Rect rect = new Rect(0, 0, width, height);
        paint.setAntiAlias(true);
        canvas.drawARGB(0, 0, 0, 0);
        paint.setColor(0xff424242);
        float radius = Math.min(width, height) / 2.0f;
        canvas.drawCircle(width / 2.0f, height / 2.0f, radius, paint);
        paint.setXfermode(new PorterDuffXfermode(PorterDuff.Mode.SRC_IN));
        canvas.drawBitmap(bitmap, rect, rect, paint);
        return output;
    }

    private static CharSequence getStyledText(String text, int color) {
        SpannableString s = new SpannableString(text);
        s.setSpan(new ForegroundColorSpan(color), 0, s.length(), Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);
        return s;
    }

    public static Bitmap decodeSampledBitmapFromResource(android.content.res.Resources res, int resId, int reqWidth,
            int reqHeight) {
        final BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        BitmapFactory.decodeResource(res, resId, options);
        options.inSampleSize = calculateInSampleSize(options, reqWidth, reqHeight);
        options.inJustDecodeBounds = false;
        return BitmapFactory.decodeResource(res, resId, options);
    }

    public static int calculateInSampleSize(BitmapFactory.Options options, int reqWidth, int reqHeight) {
        final int height = options.outHeight;
        final int width = options.outWidth;
        int inSampleSize = 1;
        if (height > reqHeight || width > reqWidth) {
            final int halfHeight = height / 2;
            final int halfWidth = width / 2;
            while ((halfHeight / inSampleSize) >= reqHeight && (halfWidth / inSampleSize) >= reqWidth) {
                inSampleSize *= 2;
            }
        }
        return inSampleSize;
    }

    public static final String ACTION_TRIGGER_NOTIF = "com.monikaafterstory.tec.es.ACTION_TRIGGER_NOTIF";

    public static void scheduleExactNotification(Context context, String title, String message, String action1,
            String action2, long delaySeconds, String jobTag, boolean sound, boolean vibration) {

        TelemetryLogger.log(context, TelemetryLogger.LEVEL_INFO, "NotificationHelper",
                "Python calling JNI -> JNI receiving Task -> Enqueuing Task",
                "Delay: " + delaySeconds + "s, JobTag: " + jobTag);

        try {
            android.app.AlarmManager am = (android.app.AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
            boolean canScheduleExact = true;

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                canScheduleExact = am.canScheduleExactAlarms();
            }

            if (canScheduleExact) {
                Intent intent = new Intent(context, ExactAlarmReceiver.class);
                intent.setAction(ACTION_TRIGGER_NOTIF);
                intent.putExtra("title", title);
                intent.putExtra("message", message);
                intent.putExtra("action1_label", action1);
                intent.putExtra("action2_label", action2);
                intent.putExtra("job_tag", jobTag);
                intent.putExtra("sound_enabled", sound);
                intent.putExtra("vibration_enabled", vibration);

                PendingIntent pi = PendingIntent.getBroadcast(context, jobTag != null ? jobTag.hashCode() : 0, intent,
                        PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);

                long triggerTime = System.currentTimeMillis() + (delaySeconds * 1000L);

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    am.setExactAndAllowWhileIdle(android.app.AlarmManager.RTC_WAKEUP, triggerTime, pi);
                } else {
                    am.setExact(android.app.AlarmManager.RTC_WAKEUP, triggerTime, pi);
                }

                TelemetryLogger.log(context, TelemetryLogger.LEVEL_INFO, "NotificationHelper",
                        "Exact alarm scheduled successfully via AlarmManager", "Target: " + triggerTime);

            } else {
                TelemetryLogger.log(context, TelemetryLogger.LEVEL_WARN, "NotificationHelper",
                        "Permission denied for EXACT_ALARM. Falling back to default WorkManager scheduling.",
                        TelemetryLogger.CODE_102);

                androidx.work.Data.Builder dataBuilder = new androidx.work.Data.Builder();
                if (title != null) dataBuilder.putString("title", title);
                if (message != null) dataBuilder.putString("message", message);
                if (action1 != null && action1.length() > 0) dataBuilder.putString("action1_label", action1);
                if (action2 != null && action2.length() > 0) dataBuilder.putString("action2_label", action2);
                if (jobTag != null) dataBuilder.putString("job_tag", jobTag);
                dataBuilder.putBoolean("sound_enabled", sound);
                dataBuilder.putBoolean("vibration_enabled", vibration);

                androidx.work.OneTimeWorkRequest workRequest = new androidx.work.OneTimeWorkRequest.Builder(NotificationWorker.class)
                        .setInputData(dataBuilder.build())
                        .setInitialDelay(delaySeconds, java.util.concurrent.TimeUnit.SECONDS)
                        .addTag(jobTag != null ? jobTag : "mas_notification")
                        .build();

                androidx.work.WorkManager.getInstance(context).enqueueUniqueWork(
                        jobTag != null ? jobTag : "mas_notification_job",
                        androidx.work.ExistingWorkPolicy.REPLACE,
                        workRequest);
            }
        } catch (SecurityException se) {
            TelemetryLogger.logError(context, "NotificationHelper", "Permission Denial when scheduling", se,
                    TelemetryLogger.CODE_101);
        } catch (Exception e) {
            TelemetryLogger.logError(context, "NotificationHelper", "Internal error scheduling notification", e,
                    TelemetryLogger.CODE_500);
        }
    }

    public static void log(Context context, String msg) {
        if (msg != null && !msg.isEmpty()) {
            TelemetryLogger.log(context, TelemetryLogger.LEVEL_INFO, "NotificationHelper_Legacy", msg, "");
        }
    }
}
