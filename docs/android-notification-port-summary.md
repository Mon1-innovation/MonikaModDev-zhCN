# Android 通知系统移植总结

日期：2026-05-08

## 目标

激活 Android 通知投递链路，并按小米通知样式文档使用系统原生通知模板与 `largeIcon` 展示 Monika 头像。

## 当前状态

通知链路已打通：

```text
Ren'Py farewell selection -> label quit -> JNI -> AlarmManager/WorkManager -> NotificationCompat UI
```

当前实现分为两层：

- 项目内 Ren'Py 桥接层：位于 `Monika After Story/game/`。
- 本机 Ren'Py SDK/RAPT Java 层：位于 `J:\Renpy\renpy-8.2.3-sdk\rapt\project\app\src\main\java\com\monikaafterstory\tec\es`。

为了避免 SDK 重装后丢失 Java 改动，当前项目也保留了一份 Java 源快照：

`docs/android-notification-java-source/`

## 1. Python/Ren'Py Bridge

`script-farewells.rpy` 已新增 farewell 选择状态：

```renpy
default mas_android_selected_farewell_label = None
```

farewell 菜单或随机 farewell 选定后，会记录对应 event label：

```renpy
$ mas_android_selected_farewell_label = _return.eventlabel
$ mas_android_selected_farewell_label = farewell.eventlabel
```

`splash.rpy` 的 `label quit` 已接入退出时调度入口：

```renpy
label quit:
    if renpy.android and mas_android_selected_farewell_label:
        $ MAS_AndroidNotifs_CheckFarewell(mas_android_selected_farewell_label)
        $ mas_android_selected_farewell_label = None
```

这条 hook 是通知能在应用退出时被调度的关键入口。

## 2. Java/UI Layer

`NotificationHelper.java` 使用系统原生通知模板：

```java
NotificationCompat.BigTextStyle
```

通知内容区域只提供昵称和文本，头像使用 Android 标准 `setLargeIcon(...)`：

```java
builder.setContentTitle(title)
       .setContentText(message)
       .setStyle(new NotificationCompat.BigTextStyle().bigText(message));

builder.setLargeIcon(circularBitmap);
```

该路线不使用 `MessagingStyle`、`Person` 或 conversation shortcut。依据小米 MIUI/HyperOS 通知样式文档，普通通知也可通过 `largeIcon` 提供联系人头像，并由系统处理应用来源标识。

## 3. Channel Architecture v7-v10

所有通知渠道都归入：

```java
new NotificationChannelGroup("mas_group", "Monika After Story")
```

当前固定渠道：

- `mas_v7`：Interactive Actions，带按钮的 farewell/交互通知。
- `mas_v8`：Birthdays，生日类通知预留渠道。
- `mas_v9`：Random Greetings，默认普通提醒/随机问候。
- `mas_v10`：Special Events，日历事件和特殊通知。

`NotificationHelper` 会在创建新渠道前清理 v1-v6 legacy channel：

```java
nm.deleteNotificationChannel(...)
```

这样可以减少系统通知设置页面中的旧渠道残留。

## 4. Native Java Localization

渠道标题和描述由 Java 根据系统语言动态选择：

```java
Locale.getDefault().getLanguage()
```

当前支持：

- English
- Spanish

其他语言回落到 English。

## 5. 图标资源和空值防护

联系人头像优先使用：

```java
monika_contact_icon
```

当前联系人头像来自项目内：

`Monika After Story/notify_icon.png`

并同步到 RAPT：

- `rapt\project\app\src\main\res\drawable-nodpi\monika_contact_icon.png`
- `rapt\prototype\app\src\main\res\drawable-nodpi\monika_contact_icon.png`

应用 launcher icon 使用：

`Monika After Story/icon.ico`

并生成到 RAPT `mipmap-*dpi/icon.png`，Manifest 继续引用：

```xml
android:icon="@mipmap/icon"
```

通知 small icon 优先使用 `@mipmap/icon`，联系人头像优先使用 `monika_contact_icon`。联系人头像 fallback 顺序：

- `notify_icon`
- `monika_profile`
- Android 系统默认图标

`setLargeIcon(...)` 有 `circularBitmap != null` 防护。头像资源缺失或解码失败时，通知仍会发出，只是不显示 Monika 头像。

## 6. Java Source Snapshot

项目内保存的 Java 源快照：

- `docs/android-notification-java-source/ExactAlarmReceiver.java`
- `docs/android-notification-java-source/NotificationActionReceiver.java`
- `docs/android-notification-java-source/NotificationHelper.java`
- `docs/android-notification-java-source/NotificationWorker.java`
- `docs/android-notification-java-source/TelemetryLogger.java`

实际 Android 编译使用本机 RAPT 目录：

`J:\Renpy\renpy-8.2.3-sdk\rapt\project\app\src\main\java\com\monikaafterstory\tec\es`

如果换机器、重装 SDK，或重新生成 RAPT 工程，需要把项目内快照同步回上述 SDK 路径。

## 7. 验证

已添加项目内源检查：

```powershell
python -m unittest tests.test_android_notification_java_source
```

该测试锁定以下关键行为：

- `BigTextStyle`
- `monika_contact_icon`
- `builder.setLargeIcon(circularBitmap)`
- 不包含 `MessagingStyle`
- 不包含 conversation shortcut / `builder.setShortcutId(...)`
- `mas_v7` 到 `mas_v10`
- `NotificationChannelGroup`
- v1-v6 cleanup
- Java locale switch

最终 Android 编译仍应运行：

```powershell
& 'J:\Renpy\renpy-8.2.3-sdk\rapt\project\gradlew.bat' -p 'J:\Renpy\renpy-8.2.3-sdk\rapt\project' :app:compileDebugJavaWithJavac
```

以及 Ren'Py 编译：

```powershell
& 'J:\Renpy\renpy-8.2.3-sdk\renpy.exe' 'J:\MAS\MonikaModDev-zhCN\Monika After Story' compile
```

## 8. Manual QA

在 Android 设备上验证：

- 游戏内开发菜单 `Android通知测试` -> `立即通知`
- `Android通知测试` -> `5秒后通知`
- 正常 farewell 后退出应用，等待对应提醒
- Android 系统通知设置中确认渠道归到 `Monika After Story`
- HyperOS / Android 上确认通知尽量呈现左侧 Monika 头像、中间标题和正文的消息通知样式
