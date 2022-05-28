<p align="center">
  <a href="https://github.com/SebastianBar/fl3xbl0w">
    <img height="100" src="logo.png" />
  </a>
</p>

## Bowflex Quirks | fl3xbl0w

### The `/sdcard/Pictures/nautilus` file

When decompiling `NautilusLauncher` you can see references to that specific path:
```java
// path: com/nautilus/nautiluslauncher/LauncherService.java
public void run() {
  if (!new File("/sdcard/Pictures/nautilus").exists()) {
    LauncherService.access$000(LauncherService.this).disableAdbDebug();
    LauncherService.access$000(LauncherService.this).enterKioskMode();
    return;
  }
  LauncherService.access$000(LauncherService.this).enableAdbDebug();
}
```

```java
// path: com/nautilus/nautiluslauncher/MainActivity.java
protected void onCreate(Bundle bundle) {
  // previous code
  if (!new File("/sdcard/Pictures/nautilus").exists()) {
    this.mPlatformControl.disableAdbDebug();
    this.mPlatformControl.enterKioskMode();
  } else {
    this.mPlatformControl.enableAdbDebug();
  }
  // more code
```

The effect of putting the file in place is that `NautilusLauncher` will actively enable adb after every restart. If the file is NOT in place, `NautilusLauncher` will actively DISABLE adb (if it was previously enabled).


### The `/sdcard/Nautilus/redbend/Credentials.txt` file

From what it looks like, [Red Bend Software](https://en.wikipedia.org/wiki/Red_Bend_Software) ([purchased by Harman](https://news.harman.com/releases/harman-completes-acquisition-of-redbend), now I get **why** so many references to KNOX) is providing OTA services for Nautilus hardware. I've found some references to that file within `com.redbend.client.apk`.

```java
package com.redbend.client;
// I'll skip some in-between code for clarity purposes
public class Ipl {
  protected static final String AUTO_SELF_REG_FILE_PATH = "Credentials.txt";
  // ...
  public static int iplGetAutoSelfRegDomainInfo(Context context, String[] strArr) {
    // ...
    File file = new File("/sdcard/Nautilus/redbend/");
    if (!file.exists()) {
      file.mkdirs();
    }
    copyAssets(context, "Credentials.txt", file.getCanonicalPath());
    bufferedReader = new BufferedReader(new FileReader(new File(file.getAbsoluteFile(), "Credentials.txt")));

```

Also on `com.redbend.client.ClientService` we can find:

```java
// ...
public class ClientService extends SmmService {
  // ...
  @Override // com.redbend.app.SmmService, android.app.Service
  public void onCreate() {
    // ...
    if (Ipl.iplGetAutoSelfRegDomainInfo(this, strArr) == 0) {
      sendEvent(new Event("D2B_AUTO_SELF_REG_INFO").addVar(new EventVar("DMA_VAR_AUTO_SELF_REG_DOMAIN_NAME", strArr[0])).addVar(new EventVar("DMA_VAR_AUTO_SELF_REG_DOMAIN_PIN", strArr[1])));
      }
```

Given that info, we can label the contents on the `/sdcard/Nautilus/redbend/Credentials.txt` as:

```
First line: DOMAIN_NAME
Second line: DOMAIN_PIN
```

*`DOMAIN_PIN` looks like an actual pin code since it is a six-digit number.*

There are some credentials within the "Red Bend Network" to match a machine with a specific brand/product for OTA updates. I expect those credentials to be IDENTICAL within all Nautilus' hardware. The file is bundled within the `com.redbend.client` APK and gets extracted upon installation.


I found references for `com.redbend.client` [over here](https://www.mdxers.org/threads/com-redbend-clent-has-stopped.175897/), and found it quite funny to see it crashing on a car. I hope it doesn't fail that often on our machines too.


### Bluetooth Heart Rate Monitor

This one was pretty easy to figure out. The Bluetooth name appears as `CL831-xxxxxxx` *(hidden number)* from [CHILEAF](https://www.chileaf.com/PRODUCTS-DETAIL?product_id=183).

Scanning it through [nRF Connect](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-mobile) exposed the devices' MAC Address and some key data:
```
Heart Rate:
UUID: 0x180D
Heart Rate Measurement
UUID: 0x2A37
```

It seemed pretty standard, and a Home Assistant Community [post](https://community.home-assistant.io/t/ble-heartrate-monitor/300354/39) already figured this one out (not the same model, but it seems the Heart Rate Monitor is using a standard protocol). I've made an ESPHome [config file](https://github.com/SebastianBar/esphome-config-files/blob/master/bowflex-hr-monitor.yaml) as a proof of concept:

![homeassistant screenshot](/assets/homeassistant-hr-sensor.png) 
