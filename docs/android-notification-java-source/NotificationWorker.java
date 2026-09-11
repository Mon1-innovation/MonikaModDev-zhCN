package com.monikaafterstory.tec.es;

import android.app.Notification;
import android.content.Context;
import android.os.PowerManager;
import android.os.BatteryManager;
import android.content.Intent;
import android.content.IntentFilter;
import androidx.annotation.NonNull;
import androidx.work.Worker;
import androidx.work.WorkerParameters;

public class NotificationWorker extends Worker {

    public NotificationWorker(@NonNull Context context, @NonNull WorkerParameters workerParams) {
        super(context, workerParams);
    }

    @NonNull
    @Override
    public Result doWork() {
        TelemetryLogger.log(getApplicationContext(), TelemetryLogger.LEVEL_INFO, "NotificationWorker", "Worker started execution", "JobId: " + getId());

        try {
            String title = getInputData().getString("title");
            String message = getInputData().getString("message");
            String action1 = getInputData().getString("action1_label");
            String action2 = getInputData().getString("action2_label");
            String jobTag = getInputData().getString("job_tag");

            boolean soundEnabled = getInputData().getBoolean("sound_enabled", true);
            boolean vibrationEnabled = getInputData().getBoolean("vibration_enabled", true);

            if (title == null) title = "Monika";
            if (message == null) message = "Hola [player]...";

            if (action1 != null && action1.length() > 0) {
                Notification notification = NotificationHelper.buildNotification(getApplicationContext(), title, message,
                        action1, action2, NotificationHelper.TYPE_INTERACTIVE, soundEnabled, vibrationEnabled, jobTag);
                android.app.NotificationManager nm = (android.app.NotificationManager) getApplicationContext()
                        .getSystemService(Context.NOTIFICATION_SERVICE);
                if (nm != null) {
                    nm.notify(NotificationHelper.NOTIFICATION_ID_STICKY, notification);
                }
            } else {
                NotificationHelper.showNotification(getApplicationContext(), 777, title, message, "", "",
                        NotificationHelper.TYPE_REMINDER, soundEnabled, vibrationEnabled, 0);
            }

            TelemetryLogger.log(getApplicationContext(), TelemetryLogger.LEVEL_INFO, "NotificationWorker", "Notification displayed successfully", "");
            return Result.success();

        } catch (Exception e) {
            TelemetryLogger.logError(getApplicationContext(), "NotificationWorker", "Failed to process work", e, TelemetryLogger.CODE_500);
            return Result.failure();
        }
    }

    @Override
    public void onStopped() {
        super.onStopped();
        Context ctx = getApplicationContext();
        
        // Registrar estado del sistema para entender por qué se detuvo (Constraints)
        PowerManager pm = (PowerManager) ctx.getSystemService(Context.POWER_SERVICE);
        boolean isDeviceIdleMode = false;
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
            if (pm != null) {
                isDeviceIdleMode = pm.isDeviceIdleMode();
            }
        }
        
        IntentFilter ifilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
        Intent batteryStatus = ctx.registerReceiver(null, ifilter);
        int status = batteryStatus != null ? batteryStatus.getIntExtra(BatteryManager.EXTRA_STATUS, -1) : -1;
        boolean isCharging = status == BatteryManager.BATTERY_STATUS_CHARGING || status == BatteryManager.BATTERY_STATUS_FULL;
        
        String metadata = "DeviceIdle: " + isDeviceIdleMode + " | Charging: " + isCharging + " | RunAttemptCount: " + getRunAttemptCount();
        
        TelemetryLogger.log(ctx, TelemetryLogger.LEVEL_WARN, "NotificationWorker", "Worker was stopped by the OS", metadata);
    }
}
