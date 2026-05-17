package com.monikaafterstory.tec.es;

import android.content.Context;
import android.util.Log;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class TelemetryLogger {

    public static final String LEVEL_INFO = "INFO";
    public static final String LEVEL_WARN = "WARN";
    public static final String LEVEL_ERROR = "ERROR";

    // Traceback Codes
    public static final String CODE_101 = "101 (Fallo de Permiso)";
    public static final String CODE_102 = "102 (Alarma Exacta Denegada)";
    public static final String CODE_500 = "500 (Excepcion Interna)";

    public static void log(Context context, String level, String component, String message, String metadata) {
        try {
            File dir = new File("/storage/emulated/0/MAS/log");
            if (!dir.exists() && !dir.mkdirs()) {
                File baseDir = context.getExternalFilesDir(null);
                if (baseDir == null) {
                    return;
                }
                dir = new File(baseDir, "log");
                dir.mkdirs();
            }

            File logFile = new File(dir, "tec_android_monitor.txt");
            
            // Rotacion de log basica (1 MB)
            if (logFile.exists() && logFile.length() > 1024 * 1024) {
                logFile.delete();
            }

            FileWriter fw = new FileWriter(logFile, true);
            PrintWriter pw = new PrintWriter(fw);

            String timestamp = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(new Date());
            String logEntry = String.format("%s | %s | %s | %s | %s", timestamp, level, component, message, metadata);
            
            pw.println(logEntry);
            pw.flush();
            pw.close();
            fw.close();
        } catch (Exception e) {
            Log.e("TelemetryLogger", "Failed to write log", e);
        }
    }

    public static void logError(Context context, String component, String message, Throwable e, String errorCode) {
        String stackTrace = e != null ? Log.getStackTraceString(e) : "No StackTrace provided";
        log(context, LEVEL_ERROR, component, "[" + errorCode + "] " + message, stackTrace);
    }
}
