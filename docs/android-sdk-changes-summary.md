# Ren'Py SDK / RAPT Android 通知改动总结

日期：2026-05-09

本文只总结针对本机 Ren'Py SDK 的改动，不包含当前 MAS 项目 `game/` 下的 Ren'Py 脚本改动。

SDK 根目录：

`J:\Renpy\renpy-8.2.3-sdk`

## 1. Java 通知实现

新增目录：

`J:\Renpy\renpy-8.2.3-sdk\rapt\project\app\src\main\java\com\monikaafterstory\tec\es`

新增/移植 Java 文件：

- `ExactAlarmReceiver.java`
- `NotificationActionReceiver.java`
- `NotificationHelper.java`
- `NotificationWorker.java`
- `TelemetryLogger.java`

来源为姊妹项目的 Android 通知系统，包名已从：

`com.tec.monikaafterstory`

改为：

`com.monikaafterstory.tec.es`

主要职责：

- `NotificationHelper`：创建通知渠道、构建通知、立即显示通知、调度延迟通知。
- `ExactAlarmReceiver`：接收 AlarmManager 精确闹钟触发，并提交 WorkManager 任务。
- `NotificationWorker`：执行延迟通知任务。
- `NotificationActionReceiver`：处理通知按钮动作，例如 dismiss。
- `TelemetryLogger`：记录通知链路日志和异常堆栈。

## 2. WorkManager 依赖

修改：

- `J:\Renpy\renpy-8.2.3-sdk\rapt\project\app\build.gradle`
- `J:\Renpy\renpy-8.2.3-sdk\rapt\templates\app-build.gradle`

加入依赖：

```gradle
implementation "androidx.work:work-runtime:2.11.2"
```

原因：

延迟通知使用 WorkManager 执行后台任务。模板文件也必须修改，否则 Ren'Py/RAPT 重新生成工程后依赖会丢失。

## 3. Android Manifest 注册

修改：

- `J:\Renpy\renpy-8.2.3-sdk\rapt\project\app\src\main\AndroidManifest.xml`
- `J:\Renpy\renpy-8.2.3-sdk\rapt\templates\app-AndroidManifest.xml`

注册 receiver：

```xml
<receiver
    android:name="com.monikaafterstory.tec.es.ExactAlarmReceiver"
    android:exported="false" />

<receiver
    android:name="com.monikaafterstory.tec.es.NotificationActionReceiver"
    android:exported="false" />
```

当前 project manifest 中还包含通知相关权限：

```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />
<uses-permission android:name="android.permission.VIBRATE" />
<uses-permission android:name="android.permission.WAKE_LOCK" />
```

注意：

`templates\app-AndroidManifest.xml` 是 RAPT 构建模板。只改 `project\app\src\main\AndroidManifest.xml` 不够，重新构建或重新生成 Android 工程时会被模板覆盖。

## 4. 图标资源

联系人头像来源：

`J:\MAS\MonikaModDev-zhCN\Monika After Story\notify_icon.png`

复制到：

- `J:\Renpy\renpy-8.2.3-sdk\rapt\project\app\src\main\res\drawable-nodpi\notify_icon.png`
- `J:\Renpy\renpy-8.2.3-sdk\rapt\prototype\app\src\main\res\drawable-nodpi\notify_icon.png`
- `J:\Renpy\renpy-8.2.3-sdk\rapt\project\app\src\main\res\drawable-nodpi\monika_contact_icon.png`
- `J:\Renpy\renpy-8.2.3-sdk\rapt\prototype\app\src\main\res\drawable-nodpi\monika_contact_icon.png`

应用 launcher icon 来源：

`J:\MAS\MonikaModDev-zhCN\Monika After Story\icon.ico`

已生成到：

- `rapt\project\app\src\main\res\mipmap-mdpi\icon.png`
- `rapt\project\app\src\main\res\mipmap-hdpi\icon.png`
- `rapt\project\app\src\main\res\mipmap-xhdpi\icon.png`
- `rapt\project\app\src\main\res\mipmap-xxhdpi\icon.png`
- `rapt\project\app\src\main\res\mipmap-xxxhdpi\icon.png`
- `rapt\prototype\app\src\main\res\mipmap-*\icon.png`

`NotificationHelper.java` 中 small icon 优先查找应用图标：

```java
context.getResources().getIdentifier("icon", "mipmap", context.getPackageName())
```

联系人头像/large icon 优先查找：

```java
context.getResources().getIdentifier("monika_contact_icon", "drawable", context.getPackageName())
```

注意：

Android 状态栏 small icon 可能被系统单色化，这是系统通知规则。展开通知里的头像/large icon 会使用 PNG 图像。

## 5. 空参数和空 bitmap 防护

修改：

`J:\Renpy\renpy-8.2.3-sdk\rapt\project\app\src\main\java\com\monikaafterstory\tec\es\NotificationHelper.java`

相关 Java 调整：

- 通知 action label 判断改为 `action != null && action.length() > 0`。
- 内部调用不再依赖 `null` 表示无按钮。
- `IconCompat.createWithBitmap(...)` 之前增加 bitmap 空值保护。

修复的崩溃：

```text
java.lang.NullPointerException:
Attempt to invoke virtual method 'java.lang.Class java.lang.Object.getClass()'
on a null object reference
at androidx.core.graphics.drawable.IconCompat.createWithBitmap
at com.monikaafterstory.tec.es.NotificationHelper.buildNotification
```

当前行为：

如果 `monika_contact_icon`、`notify_icon` 或 fallback 图像资源解码失败，通知仍会继续构建，只是不设置 `Person` icon / large icon。

## 6. Conversation UI 和 v7-v10 渠道

`NotificationHelper.java` 已完成 Android 11+ conversation notification 现代化：

- 使用 `NotificationCompat.MessagingStyle` 替换 legacy big text 展示。
- 使用 `androidx.core.app.Person` 表示 Monika。
- 使用 `ShortcutInfoCompat` / `ShortcutManagerCompat.pushDynamicShortcut(...)` 注册 `monika_chat_shortcut`。
- 通知构建时调用 `builder.setShortcutId("monika_chat_shortcut")`。

固定通知渠道：

- `mas_v7`：Interactive Actions，带按钮通知。
- `mas_v8`：Birthdays，生日通知。
- `mas_v9`：Random Greetings，默认普通通知。
- `mas_v10`：Special Events，日历和特殊事件通知。

所有渠道归入：

```java
new NotificationChannelGroup("mas_group", "Monika After Story")
```

Java 层会调用 `deleteNotificationChannel(...)` 清理 v1-v6 legacy channel，并使用：

```java
Locale.getDefault().getLanguage()
```

为渠道标题/描述选择 English 或 Spanish。

项目内也保存了一份 Java 源快照：

`J:\MAS\MonikaModDev-zhCN\docs\android-notification-java-source`

如果 SDK 重装或 RAPT 工程被重新生成，应从该目录恢复 Java 源。

## 7. Gradle JVM 稳定性配置

修改：

- `J:\Renpy\renpy-8.2.3-sdk\rapt\project\gradle.properties`
- `J:\Renpy\renpy-8.2.3-sdk\rapt\prototype\gradle.properties`

当前关键配置：

```properties
org.gradle.jvmargs=-Xmx1536m -XX:MaxMetaspaceSize=512m -Dfile.encoding=UTF-8
org.gradle.workers.max=4
org.gradle.vfs.watch=false
```

原因：

之前构建出现 JVM crash log：

`J:\Renpy\renpy-8.2.3-sdk\rapt\hs_err_pid10144.log`

分析为 Gradle/JVM daemon 内存或 native mmap 失败，而不是通知 Java 编译错误。调整后降低 Gradle daemon 堆内存、限制 worker 数量，并关闭 VFS watch，减少 Windows 下资源压力。

## 8. 日志行为

Java 通知层使用 `TelemetryLogger` 输出链路日志，格式类似：

```text
2026-05-06 21:23:08 | INFO | NotificationHelper | Python calling JNI -> JNI receiving Task -> Enqueuing Task | Delay: 5s, JobTag: mas_notification
```

已确认日志能覆盖：

- JNI 调用进入 Java。
- 延迟通知调度。
- Exact Alarm 注册。
- Alarm 触发。
- WorkManager 入队。
- Worker 执行。
- Java 异常堆栈。

这些日志用于定位过一次延迟通知崩溃，确认 AlarmManager 和 WorkManager 链路正常，问题在通知对象构建阶段。

## 9. 已验证命令

已运行：

```powershell
& 'J:\Renpy\renpy-8.2.3-sdk\rapt\project\gradlew.bat' -p 'J:\Renpy\renpy-8.2.3-sdk\rapt\project' :app:compileDebugJavaWithJavac
```

结果：

```text
BUILD SUCCESSFUL
```

构建中仍有既存 warning：

- Manifest 中部分权限重复，例如 `VIBRATE`、`INTERNET`、`WRITE_EXTERNAL_STORAGE`、`MANAGE_EXTERNAL_STORAGE`。
- Java 21 编译 source/target 8 的弃用警告。

这些 warning 未阻塞构建。

## 10. 重装或迁移 SDK 时需要恢复的清单

如果更换机器、重装 Ren'Py SDK，或重新初始化 RAPT，需要恢复以下 SDK 文件/目录：

- `rapt\project\app\src\main\java\com\monikaafterstory\tec\es\*.java`
- `rapt\project\app\src\main\res\drawable-nodpi\notify_icon.png`
- `rapt\project\app\src\main\res\drawable-nodpi\monika_contact_icon.png`
- `rapt\prototype\app\src\main\res\drawable-nodpi\notify_icon.png`
- `rapt\prototype\app\src\main\res\drawable-nodpi\monika_contact_icon.png`
- `rapt\project\app\src\main\res\mipmap-*\icon.png`
- `rapt\project\app\src\main\res\mipmap-*\icon_background.png`
- `rapt\project\app\src\main\res\mipmap-*\icon_foreground.png`
- `rapt\prototype\app\src\main\res\mipmap-*\icon.png`
- `rapt\prototype\app\src\main\res\mipmap-*\icon_background.png`
- `rapt\prototype\app\src\main\res\mipmap-*\icon_foreground.png`
- `rapt\project\app\build.gradle`
- `rapt\templates\app-build.gradle`
- `rapt\project\app\src\main\AndroidManifest.xml`
- `rapt\templates\app-AndroidManifest.xml`
- `rapt\project\gradle.properties`
- `rapt\prototype\gradle.properties`

最重要的是模板文件：

- `rapt\templates\app-AndroidManifest.xml`
- `rapt\templates\app-build.gradle`

因为 RAPT 构建/生成工程时会从模板生成 project 文件，模板缺失会导致 receiver 或 WorkManager 依赖丢失。
