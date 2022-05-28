<p align="center">
  <img height="100" src="logo.png">
</p>

## Backup your Console contents | fl3xbl0w

After being freed from `AppMonitorService` (or after any OTA update is received), the first thing to do is back up as much data as possible.

Make sure you're already connected to the tablet:
> `adb connect <Tablet IP Address>`

## Backup /sdcard contents

It may contain some required files for the machine to work properly after a factory reset (mainly on the `/sdcard/Android` and `/sdcard/Nautilus` folders). We'll back up everything with:

> `adb pull /sdcard/ .`


## Backup APKs

First, get the list of all packages installed on the tablet (just for you to have a reference):

> `adb shell pm list packages -f`

They will appear in the following format: `package:<APK location>=<package name>`

You'll have to find the apps you want to backup. NOT ALL APPS ARE REQUIRED, most of them are stock Android apps, and so we'll only search for "non-stock apps" through some filtering:

> `adb shell pm list packages -f | grep -wviE 'com.android|com.google|framework-res|/vendor/overlay'`

You'll be able to see records for apps from `com.nautilus`, `com.redbend`, `com.netflix`, `com.amazon`, `com.disney` and maybe some more in the future. We'll want to back up everything we see on that list (unique ID's hidden, use your own results):

```
> adb shell pm list packages -f | grep -wviE 'com.android|com.google|framework-res|/vendor/overlay'
package:/data/app/com.nautilus.sbctest-XXXXXXXXXXXXXXXX/base.apk=com.nautilus.sbctest
package:/data/app/com.redbend.client-XXXXXXXXXXXXXXXX/base.apk=com.redbend.client
package:/data/app/com.nautilus.nlssbcsystemsettings-XXXXXXXXXXXXXXXX/base.apk=com.nautilus.nlssbcsystemsettings
package:/system/priv-app/RBDualPartService/RBDualPartService.apk=com.redbend.dualpart.service.app
package:/data/app/com.netflix.mediaclient-XXXXXXXXXXXXXXXX/base.apk=com.netflix.mediaclient
package:/data/app/com.nautilus.nautiluslauncher-XXXXXXXXXXXXXXXX/base.apk=com.nautilus.nautiluslauncher
package:/data/app/com.amazon.avod.thirdpartyclient-XXXXXXXXXXXXXXXX/base.apk=com.amazon.avod.thirdpartyclient
package:/data/app/com.nautilus.sbc_demo_app-XXXXXXXXXXXXXXXX/base.apk=com.nautilus.sbc_demo_app
package:/data/app/com.nautilus.UtilityApp-XXXXXXXXXXXXXXXX/base.apk=com.nautilus.UtilityApp
package:/data/app/com.nautilus.g4assetmanager-XXXXXXXXXXXXXXXX/base.apk=com.nautilus.g4assetmanager
package:/data/app/com.nautilus.platform_hardwaretest-XXXXXXXXXXXXXXXX/base.apk=com.nautilus.platform_hardwaretest
package:/data/app/com.nautilus.webviewer-XXXXXXXXXXXXXXXX/base.apk=com.nautilus.webviewer
package:/data/app/com.nautilus.bowflex.usb-XXXXXXXXXXXXXXXX/base.apk=com.nautilus.bowflex.usb
package:/data/app/com.disney.disneyplus-XXXXXXXXXXXXXXXX/base.apk=com.disney.disneyplus
```

> NOTE: `com.redbend.dualpart.service.app` comes from `/system/priv-app/`, meaning that it will remain installed even after a factory reset. We can dump it anyways if you are interested in reverse engineering the apps.


Let's take Disney Plus as an example (unique ID hidden)
```
package:/data/app/com.disney.disneyplus-XXXXXXXXXXXXXXXX/base.apk=com.disney.disneyplus
```

That line, based on the format I've mentioned, would be:
```
Package location: /data/app/com.disney.disneyplus-XXXXXXXXXXXXXXXX/base.apk
Package name: com.disney.disneyplus
```

We'll search for which version of the app we have with that info. Let's use the Package name that we've just identified and run:

> `adb shell dumpsys package com.disney.disneyplus | grep versionName`

In my case, I've received:
```
> adb shell dumpsys package com.disney.disneyplus | grep versionName
    versionName=2.4.2-rc2
```

Now, to create a backup for the Disney Plus package, the procedure would be:

> `adb pull /data/app/com.disney.disneyplus-XXXXXXXXXXXXXXXX/base.apk .`

Immediately after it finishes, go through your File Explorer and rename the just dumped `base.apk` file into `com.disney.disneyplus-2.4.2-rc2.apk`.

The format for APKs that I suggest, given that example, is: `<Package name>-<version>.apk`

Now repeat the process for the rest of the apps.


## Backup AppData
This seems to be able to backup *some (not sure if all)* AppData.

*Note that not all installed apps generate AppData, or we, as the `shell` user, may not have permissions to backup everything.*

Create a full backup of all user-installed apps:

> `adb backup -f appdata.adb -all -noapk -nosystem`

Alternatively, you can have the same output from an alternative command:

> `adb shell 'bu backup -all -noapk -nosystem' > appdata.adb`

Both commands will request an "in-screen confirmation" that you want to do a backup. Touch on "**BACK UP MY DATA**":
![backup confirmation screen](/assets/dialog-backup-confirm.png) 

If you want to extract the contents (on Linux, macOS), you'll need `zlib-flate` from [qpdf](https://command-not-found.com/qpdf) and run:

> `dd if=appdata.adb bs=24 skip=1 | zlib-flate -uncompress | tar xf -`


There is some fascinating data for `com.nautilus.bowflex.usb`.
There is Personally identifiable information (PII) inside, so **make sure to double-check what files you share**.


*These backup and extraction methods are from [this Gist](https://gist.github.com/AnatomicJC/e773dd55ae60ab0b2d6dd2351eb977c1). I've only tested the Backup methods listed there, which are safe to play. **If you play with the Gist Restore, you're on your own**. Let us know if it works tho!*


## Script

I developed a [Python script](dump.py) for dumping some contents (it doesn't include AppData for now). **Only tested on macOS with android-platform-tools installed through brew**. Read the script, and be sure it makes sense to you before running.
