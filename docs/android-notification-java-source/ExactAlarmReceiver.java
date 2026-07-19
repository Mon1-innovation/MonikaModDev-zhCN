package com.monikaafterstory.tec.es;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import androidx.work.Data;
import androidx.work.ExistingWorkPolicy;
import androidx.work.OneTimeWorkRequest;
import androidx.work.OutOfQuotaPolicy;
import androidx.work.WorkManager;

public class ExactAlarmReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent == null || !NotificationHelper.ACTION_TRIGGER_NOTIF.equals(intent.getAction())) {
            return;
        }

        TelemetryLogger.log(context, TelemetryLogger.LEVEL_INFO, "ExactAlarmReceiver", 
            "Alarm triggered, enqueuing Expedited WorkManager task.", "Action: " + intent.getAction());

        try {
            String title = intent.getStringExtra("title");
            String message = intent.getStringExtra("message");
            String action1 = intent.getStringExtra("action1_label");
            String action2 = intent.getStringExtra("action2_label");
            String jobTag = intent.getStringExtra("job_tag");
            boolean soundEnabled = intent.getBooleanExtra("sound_enabled", true);
            boolean vibrationEnabled = intent.getBooleanExtra("vibration_enabled", true);

            Data.Builder dataBuilder = new Data.Builder();
            if (title != null) dataBuilder.putString("title", title);
            if (message != null) dataBuilder.putString("message", message);
            if (action1 != null && action1.length() > 0) dataBuilder.putString("action1_label", action1);
            if (action2 != null && action2.length() > 0) dataBuilder.putString("action2_label", action2);
            if (jobTag != null) dataBuilder.putString("job_tag", jobTag);
            dataBuilder.putBoolean("sound_enabled", soundEnabled);
            dataBuilder.putBoolean("vibration_enabled", vibrationEnabled);

            OneTimeWorkRequest workRequest = new OneTimeWorkRequest.Builder(NotificationWorker.class)
                    .setInputData(dataBuilder.build())
                    .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
                    .addTag(jobTag != null ? jobTag : "mas_notification")
                    .build();

            WorkManager.getInstance(context).enqueueUniqueWork(
                    "mas_notification_job_expedited", 
                    ExistingWorkPolicy.REPLACE, 
                    workRequest
            );

            TelemetryLogger.log(context, TelemetryLogger.LEVEL_INFO, "ExactAlarmReceiver", 
                "WorkManager task enqueued successfully.", "JobTag: " + jobTag);

        } catch (Exception e) {
            TelemetryLogger.logError(context, "ExactAlarmReceiver", "Failed to enqueue expedited work", e, TelemetryLogger.CODE_500);
        }
    }
}
