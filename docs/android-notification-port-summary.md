# Android 通知系统移植总结

日期：2026-05-08

## 目标

激活 Android 通知投递链路，并将通知 UI/UX 更新到 Android 11+ 的 conversation notification 风格。

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

`NotificationHelper.java` 已从 legacy `BigTextStyle` 迁移到：

```java
NotificationCompat.MessagingStyle
```

通知现在使用 Monika 的 `Person` 信息构建 conversation-style UI，并注册系统 conversation shortcut：

```java
ShortcutInfoCompat shortcut = new ShortcutInfoCompat.Builder(context, "monika_chat_shortcut")
    .setPerson(monikaUser)
    .setCategories(categories) // android.shortcut.conversation
    .build();
ShortcutManagerCompat.pushDynamicShortcut(context, shortcut);
builder.setShortcutId("monika_chat_shortcut");
```

这会让 Android 11+ 将通知归类为对话，提升头像和会话展示优先级。

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

通知 small icon 优先使用 `@mipmap/icon`，联系人头像/large icon 优先使用 `monika_contact_icon`。联系人头像 fallback 顺序：

- `notify_icon`
- `monika_profile`
- Android 系统默认图标

`IconCompat.createWithBitmap(...)` 和 `setLargeIcon(...)` 都有 `circularBitmap != null` 防护。头像资源缺失或解码失败时，通知仍会发出，只是不显示头像大图。

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

- `MessagingStyle`
- conversation shortcut
- `builder.setShortcutId("monika_chat_shortcut")`
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
- Android 11+ 上确认通知以 conversation 样式显示 Monika 头像
