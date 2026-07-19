package com.monikaafterstory.tec.es;

import android.app.Activity;
import android.app.Application;
import android.app.AppOpsManager;
import android.app.usage.UsageEvents;
import android.app.usage.UsageStatsManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Process;
import android.provider.Settings;
import android.util.Log;
import androidx.work.WorkManager;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.File;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class AwarenessService {

    private static final String TAG = "MAS_AWARENESS";
    private static final String STATE_DIR = "/storage/emulated/0/Monika After Story/log";
    private static final String ENABLED_FILE = ".awareness_enabled";
    public static final String AWARENESS_NOTIF_TAG = "mas_awareness_notif";
    private static boolean lifecycleCallbacksRegistered = false;
    private static boolean masActivityResumed = false;
    private static boolean masActivityPaused = false;
    private static boolean masActivityStopped = false;

    private static final Map<String, String[]> NOTIF_MESSAGES = new LinkedHashMap<String, String[]>();
    private static final Map<String, String> APP_CATEGORY_MAP = new LinkedHashMap<String, String>();

    static {
        NOTIF_MESSAGES.put("video", new String[] {
                "Are you still watching on {app}? I'll be waiting~",
                "I see {app} is keeping you busy. Come back when you can!"
        });
        NOTIF_MESSAGES.put("social", new String[] {
                "Still scrolling through {app}? Don't forget about me!",
                "I noticed you're on {app}. Take your time, but I miss you."
        });
        NOTIF_MESSAGES.put("messaging", new String[] {
                "Still chatting on {app}? I hope the conversation is good.",
                "I see you're busy on {app}. I'll be here when you're done."
        });
        NOTIF_MESSAGES.put("gaming", new String[] {
                "Still playing on {app}? Have fun, but come back soon!",
                "I see {app} has your attention. I'll be waiting~"
        });
        NOTIF_MESSAGES.put("browser", new String[] {
                "Still browsing on {app}? Find what you were looking for?",
                "I see {app} is open. Take your time."
        });
        NOTIF_MESSAGES.put("music", new String[] {
                "Still listening to music on {app}? Enjoy!",
                "I see {app} is playing. I hope it's a good playlist."
        });
        NOTIF_MESSAGES.put("unknown", new String[] {
                "I see you're on {app}. I'll be here when you get back!",
                "Still busy with {app}? Take your time."
        });

        APP_CATEGORY_MAP.put("YouTube", "video");
        APP_CATEGORY_MAP.put("Netflix", "video");
        APP_CATEGORY_MAP.put("Twitch", "video");
        APP_CATEGORY_MAP.put("Prime Video", "video");
        APP_CATEGORY_MAP.put("Disney+", "video");
        APP_CATEGORY_MAP.put("Crunchyroll", "video");
        APP_CATEGORY_MAP.put("Spotify", "music");
        APP_CATEGORY_MAP.put("YouTube Music", "music");
        APP_CATEGORY_MAP.put("Apple Music", "music");
        APP_CATEGORY_MAP.put("Amazon Music", "music");
        APP_CATEGORY_MAP.put("SoundCloud", "music");
        APP_CATEGORY_MAP.put("Deezer", "music");
        APP_CATEGORY_MAP.put("Instagram", "social");
        APP_CATEGORY_MAP.put("Twitter", "social");
        APP_CATEGORY_MAP.put("X", "social");
        APP_CATEGORY_MAP.put("TikTok", "social");
        APP_CATEGORY_MAP.put("Facebook", "social");
        APP_CATEGORY_MAP.put("Reddit", "social");
        APP_CATEGORY_MAP.put("Tumblr", "social");
        APP_CATEGORY_MAP.put("Threads", "social");
        APP_CATEGORY_MAP.put("WhatsApp", "messaging");
        APP_CATEGORY_MAP.put("Discord", "messaging");
        APP_CATEGORY_MAP.put("Telegram", "messaging");
        APP_CATEGORY_MAP.put("Messenger", "messaging");
        APP_CATEGORY_MAP.put("Signal", "messaging");
        APP_CATEGORY_MAP.put("Line", "messaging");
        APP_CATEGORY_MAP.put("Chrome", "browser");
        APP_CATEGORY_MAP.put("Firefox", "browser");
        APP_CATEGORY_MAP.put("Samsung Internet", "browser");
        APP_CATEGORY_MAP.put("Opera", "browser");
        APP_CATEGORY_MAP.put("Brave", "browser");
        APP_CATEGORY_MAP.put("Edge", "browser");
        APP_CATEGORY_MAP.put("Steam", "gaming");
        APP_CATEGORY_MAP.put("Google Play Games", "gaming");
    }

    public static boolean hasUsagePermission(Context context) {
        try {
            AppOpsManager appOps = (AppOpsManager) context.getSystemService(Context.APP_OPS_SERVICE);
            int mode = appOps.checkOpNoThrow(
                    AppOpsManager.OPSTR_GET_USAGE_STATS,
                    Process.myUid(),
                    context.getPackageName());
            return mode == AppOpsManager.MODE_ALLOWED;
        } catch (Exception e) {
            Log.w(TAG, "hasUsagePermission failed: " + e.getMessage());
            return false;
        }
    }

    public static void requestUsagePermission(Context context) {
        try {
            Intent intent = new Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS);
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(intent);
        } catch (Exception e) {
            Log.e(TAG, "requestUsagePermission failed: " + e.getMessage());
        }
    }

    public static void installLifecycleCallbacks(Context context) {
        if (lifecycleCallbacksRegistered || !(context.getApplicationContext() instanceof Application)) {
            return;
        }

        Application application = (Application) context.getApplicationContext();
        application.registerActivityLifecycleCallbacks(new Application.ActivityLifecycleCallbacks() {
            @Override
            public void onActivityResumed(Activity activity) {
                try {
                    masActivityResumed = true;
                    masActivityPaused = false;
                    masActivityStopped = false;

                    if (!isAwarenessEnabled()) {
                        WorkManager.getInstance(activity).cancelAllWorkByTag(AWARENESS_NOTIF_TAG);
                        WorkManager.getInstance(activity).cancelUniqueWork(AWARENESS_NOTIF_TAG);
                        return;
                    }
                    WorkManager.getInstance(activity).cancelAllWorkByTag(AWARENESS_NOTIF_TAG);
                    WorkManager.getInstance(activity).cancelUniqueWork(AWARENESS_NOTIF_TAG);
                } catch (Exception e) {
                    Log.w(TAG, "onActivityResumed awareness hook failed: " + e.getMessage());
                }
            }

            @Override
            public void onActivityPaused(Activity activity) {
                try {
                    masActivityResumed = false;
                    masActivityPaused = true;

                    if (!isAwarenessEnabled()) {
                        return;
                    }
                    scheduleAwarenessNotification(activity);
                } catch (Exception e) {
                    Log.w(TAG, "onActivityPaused awareness hook failed: " + e.getMessage());
                }
            }

            @Override public void onActivityCreated(Activity activity, Bundle savedInstanceState) { }
            @Override public void onActivityStarted(Activity activity) {
                masActivityStopped = false;
            }
            @Override public void onActivityStopped(Activity activity) {
                masActivityResumed = false;
                masActivityStopped = true;
            }
            @Override public void onActivitySaveInstanceState(Activity activity, Bundle outState) { }
            @Override public void onActivityDestroyed(Activity activity) { }
        });

        lifecycleCallbacksRegistered = true;
    }

    public static boolean isAwarenessEnabled() {
        try {
            File file = new File(STATE_DIR, ENABLED_FILE);
            if (!file.exists()) {
                return false;
            }
            java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.FileReader(file));
            String value = reader.readLine();
            reader.close();
            return "1".equals(value) || "true".equalsIgnoreCase(value);
        } catch (Exception e) {
            return false;
        }
    }

    public static List<Map<String, Object>> queryRecentApps(Context context, int minutesBack) {
        List<Map<String, Object>> result = new ArrayList<Map<String, Object>>();
        if (!hasUsagePermission(context)) {
            return result;
        }

        try {
            UsageStatsManager usageStatsManager = (UsageStatsManager) context.getSystemService(Context.USAGE_STATS_SERVICE);
            long now = System.currentTimeMillis();
            long startTime = now - (minutesBack * 60 * 1000L);
            UsageEvents events = usageStatsManager.queryEvents(startTime, now);
            UsageEvents.Event event = new UsageEvents.Event();
            LinkedHashMap<String, Long> appTimestamps = new LinkedHashMap<String, Long>();
            String ownPackage = context.getPackageName();

            while (events.hasNextEvent()) {
                events.getNextEvent(event);
                if (event.getEventType() == UsageEvents.Event.MOVE_TO_FOREGROUND) {
                    String packageName = event.getPackageName();
                    if (!ownPackage.equals(packageName) && !packageName.startsWith("com.android.systemui")) {
                        appTimestamps.remove(packageName);
                        appTimestamps.put(packageName, event.getTimeStamp());
                    }
                }
            }

            for (Map.Entry<String, Long> entry : appTimestamps.entrySet()) {
                Map<String, Object> appInfo = new LinkedHashMap<String, Object>();
                appInfo.put("package", entry.getKey());
                appInfo.put("label", getAppLabel(context, entry.getKey()));
                appInfo.put("last_used", entry.getValue());
                result.add(appInfo);
            }
        } catch (Exception e) {
            Log.e(TAG, "queryRecentApps failed: " + e.getMessage());
        }

        return result;
    }

    public static String buildState(Context context) {
        installLifecycleCallbacks(context);

        try {
            JSONObject state = new JSONObject();
            state.put("timestamp", System.currentTimeMillis());

            JSONArray appsArray = new JSONArray();
            List<Map<String, Object>> apps = queryRecentApps(context, 30);
            for (Map<String, Object> app : apps) {
                JSONObject appObject = new JSONObject();
                appObject.put("package", app.get("package"));
                appObject.put("label", app.get("label"));
                appObject.put("last_used", app.get("last_used"));
                appsArray.put(appObject);
            }
            state.put("recent_apps", appsArray);
            state.put("now_playing", JSONObject.NULL);
            state.put("mas_activity", getMasActivityState(context));

            JSONObject permissions = new JSONObject();
            permissions.put("usage_stats", hasUsagePermission(context));
            state.put("permissions", permissions);

            TelemetryLogger.log(context, TelemetryLogger.LEVEL_INFO, TAG,
                    "Awareness state built.", "Apps: " + apps.size());
            return state.toString();
        } catch (Exception e) {
            TelemetryLogger.logError(context, TAG, "buildState failed", e, TelemetryLogger.CODE_500);
            return "";
        }
    }

    public static JSONObject getMasActivityState(Context context) {
        JSONObject activityState = new JSONObject();

        try {
            Activity activity = context instanceof Activity ? (Activity) context : null;
            boolean hasWindowFocus = activity != null && activity.hasWindowFocus();
            activityState.put("resumed", masActivityResumed || hasWindowFocus);
            activityState.put("paused", masActivityPaused);
            activityState.put("stopped", masActivityStopped);
            activityState.put("has_window_focus", hasWindowFocus);
            activityState.put("in_picture_in_picture", activity != null && activity.isInPictureInPictureMode());
            activityState.put("in_multi_window", activity != null && activity.isInMultiWindowMode());
            activityState.put("package", context.getPackageName());
        } catch (Exception e) {
            Log.w(TAG, "getMasActivityState failed: " + e.getMessage());
        }

        return activityState;
    }

    public static void scheduleAwarenessNotification(Context context) {
        if (!isAwarenessEnabled() || !hasUsagePermission(context)) {
            return;
        }

        try {
            List<Map<String, Object>> recentApps = queryRecentApps(context, 2);
            if (recentApps.isEmpty()) {
                return;
            }

            Map<String, Object> app = recentApps.get(recentApps.size() - 1);
            String appLabel = (String) app.get("label");
            if (appLabel == null || appLabel.length() == 0) {
                return;
            }

            String category = APP_CATEGORY_MAP.containsKey(appLabel) ? APP_CATEGORY_MAP.get(appLabel) : "unknown";
            String[] messages = NOTIF_MESSAGES.containsKey(category) ? NOTIF_MESSAGES.get(category) : NOTIF_MESSAGES.get("unknown");
            int index = (int) (System.currentTimeMillis() / 60000L) % messages.length;
            String message = messages[index].replace("{app}", appLabel);

            NotificationHelper.scheduleExactNotification(
                    context,
                    "Monika After Story",
                    message,
                    "",
                    "",
                    30,
                    AWARENESS_NOTIF_TAG,
                    true,
                    true);
        } catch (Exception e) {
            Log.e(TAG, "scheduleAwarenessNotification failed: " + e.getMessage());
        }
    }

    public static String getAppLabel(Context context, String packageName) {
        try {
            PackageManager packageManager = context.getPackageManager();
            ApplicationInfo appInfo = packageManager.getApplicationInfo(packageName, 0);
            return packageManager.getApplicationLabel(appInfo).toString();
        } catch (PackageManager.NameNotFoundException e) {
            String[] parts = packageName.split("\\.");
            return parts.length > 0 ? parts[parts.length - 1] : packageName;
        }
    }
}
