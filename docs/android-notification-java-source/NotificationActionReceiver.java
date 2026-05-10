package com.monikaafterstory.tec.es;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import androidx.work.WorkManager;

public class NotificationActionReceiver extends BroadcastReceiver {

    public static final String ACTION_DISMISS = "com.monikaafterstory.tec.es.ACTION_DISMISS";

    @Override
    public void onReceive(Context context, Intent intent) {
        try {
            String action = intent.getAction();

            if (ACTION_DISMISS.equals(action)) {
                int notifId = intent.getIntExtra("notification_id", -1);
                if (notifId != -1) {
                    android.app.NotificationManager nm = (android.app.NotificationManager) context
                            .getSystemService(Context.NOTIFICATION_SERVICE);
                    if (nm != null) {
                        nm.cancel(notifId);
                    }
                }
                WorkManager wm = WorkManager.getInstance(context);
                wm.cancelAllWorkByTag("mas_notification");
                wm.cancelAllWorkByTag("TYPE_SLEEP");
            }

        } catch (Exception e) {
        }
    }
}