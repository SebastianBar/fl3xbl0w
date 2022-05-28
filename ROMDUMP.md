<p align="center">
  <img height="100" src="logo.png">
</p>

## ROM Dump | fl3xbl0w

### Rockchip Loader Mode | fl3xbl0w

An RK3399 processor powers the Android hardware. Rockchip processors come with a "loader mode" as a standard feature.

The toolset that I've used is:
- Rockchip Driver Assistant v4.5 from [ChinaGadgetsReviews](https://chinagadgetsreviews.com/?s=Rockchip+Driver+Assistant)
- rkDumper 1.09 test from [this XDA post](https://forum.xda-developers.com/t/tool-rkdumper-utility-for-backup-firmware-of-rockchips-devices.2915363/page-9#post-84229591)
- Android Tool Release v2.69 from [ChinaGadgetsReviews](https://chinagadgetsreviews.com/?s=android+tool+release)

*There is a newer driver version available for download, but it's known to be incompatible with rkDumper.*

In order to play with this, you'll have to unmount the Bowflex Console, unscrew the plastic back cover, and mount it back in a "naked form".
**Do not attempt this, as playing with the Android hardware in Loader Mode can lead to a permanently bricked device.**

![console mounted with back cover removed](/assets/console-mounted.jpg)

Here are the relevant parts of the Android logic board for Rockchip stuff:
![vantron pcb](/assets/vantron-pcb.jpg)

You can have the Android Tool Release app opened at all times as a reference to check on which mode the tablet is at.

With the machine turned on in "normal mode" and plugging it into a computer, it identifies itself as `NFTM-LAR`:
```
NFTM-LAR:
  Product ID: 0x0001
  Vendor ID: 0x2207 (Fuzhou Rockchip Electronics Co., Ltd.)
  Version: 3.10
  Speed: Up to 480 Mb/s
  Manufacturer: Vanzo
  Location ID: 0x14120000 / 9
  Current Available (mA): 500
  Current Required (mA): 500
  Extra Operating Current (mA): 0
```

Having the machine turned off, plugged in through USB to a computer, keeping the "Recovery button" pressed and turning it on, it should boot in "Loader mode". The machine will "chime", but the screen will remain static. *You can turn off, wait a minute, turn it on, and the machine will boot normally.*

*The Android hardware does not handle the "chime" after turning the machine on, but through Nautilus' other PCB's.*

It will now report itself in the computer as `USB download gadget` (hidden Serial Number):
```
USB download gadget:
  Product ID: 0x330c
  Vendor ID: 0x2207 (Fuzhou Rockchip Electronics Co., Ltd.)
  Version: 99.99
  Serial Number: XXXXXXXXXXXXXXX
  Manufacturer: Rockchip
  Location ID: 0x14120000
```

After running rkDumper against the console, we get some information regarding partitions:
```
"EFI PART" sign found (RKFP FW dump)

Partition "EFI_part" (0x00004000) saved (format: RockChip RKFP dump)
Partition "uboot_a" (0x00002000) saved (format: Rockchip uboot image file)
Partition "uboot_b" (0x00002000) saved (format: Rockchip uboot image file)
Partition "trust_a" (0x00002000) saved (format: unknown)
Partition "trust_b" (0x00002000) saved (format: unknown)
Partition "misc" (0x00002000) saved (format: unknown)
Partition "resource" (0x00008000) saved (format: unknown)
Partition "kernel" (0x00010000) saved (format: unknown)
Partition "dtb" (0x00002000) saved (format: unknown)
Partition "dtbo_a" (0x00002000) saved (format: unknown)
Partition "dtbo_b" (0x00002000) saved (format: unknown)
Partition "vbmeta_a" (0x00000800) saved (format: unknown)
Partition "vbmeta_b" (0x00000800) saved (format: unknown)
Partition "boot_a" (0x00020000) saved (format: unknown)
Partition "boot_b" (0x00020000) saved (format: unknown)
Partition "backup" (0x00038000) saved (format: unknown)
Partition "security" (0x00002000) saved (format: unknown)
Partition "cache" (0x00100000) saved (format: unknown)
Partition "system_a" (0x00500000) saved (format: unknown)
Partition "system_b" (0x00500000) saved (format: unknown)
Partition "metadata" (0x00008000) saved (format: unknown)
Partition "vendor_a" (0x00100000) saved (format: unknown)
Partition "vendor_b" (0x00100000) saved (format: unknown)
Partition "oem_a" (0x00100000) saved (format: unknown)
Partition "oem_b" (0x00100000) saved (format: unknown)
Partition "frp" (0x00000400) saved (format: unknown)
Partition "sw_release" (0x00ed7000) saved (format: unknown)
Partition "video" (0x0047e000) saved (format: unknown)
Partition "userdata" (0x0169bbdf) saved (format: unknown)
```

`uboot_a` and `uboot_b` were successfully extracted, but all other partitions marked as `(format: unknown)` are improperly dumped, only extracting hex `CC` values from it.

A similar case to mine was documented over [4pda](https://4pda.to/forum/index.php?s=&showtopic=614530&view=findpost&p=102427030), and after [asking](https://forum.xda-developers.com/t/tool-rkdumper-utility-for-backup-firmware-of-rockchips-devices.2915363/page-11#post-86678625) the developer of rkDumper, [he says](https://forum.xda-developers.com/t/tool-rkdumper-utility-for-backup-firmware-of-rockchips-devices.2915363/page-11#post-86687085) a new RockChip loader must be in place. Going through this method seems to be a no-go for now.


### ADB | fl3xbl0w

Some similar data can be found through adb, but no dump seems to be possible as we lack root permissions:

```
> ls -al /dev/block/platform/
total 0
drwxr-xr-x 3 root root   60 2022-04-13 19:38 .
drwxr-xr-x 5 root root 1300 2022-04-13 19:38 ..
drwxr-xr-x 3 root root  700 2022-04-13 19:38 fe330000.sdhci
```

```
> ls -al /dev/block/platform/fe330000.sdhci/by-name/
total 0
drwxr-xr-x 2 root root 600 2022-04-13 19:38 .
drwxr-xr-x 3 root root 700 2022-04-13 19:38 ..
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 backup -> /dev/block/mmcblk0p15
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 boot_a -> /dev/block/mmcblk0p13
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 boot_b -> /dev/block/mmcblk0p14
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 cache -> /dev/block/mmcblk0p17
lrwxrwxrwx 1 root root  20 2022-04-13 19:38 dtb -> /dev/block/mmcblk0p8
lrwxrwxrwx 1 root root  20 2022-04-13 19:38 dtbo_a -> /dev/block/mmcblk0p9
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 dtbo_b -> /dev/block/mmcblk0p10
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 frp -> /dev/block/mmcblk0p25
lrwxrwxrwx 1 root root  20 2022-04-13 19:38 kernel -> /dev/block/mmcblk0p7
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 metadata -> /dev/block/mmcblk0p20
lrwxrwxrwx 1 root root  20 2022-04-13 19:38 misc -> /dev/block/mmcblk0p5
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 oem_a -> /dev/block/mmcblk0p23
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 oem_b -> /dev/block/mmcblk0p24
lrwxrwxrwx 1 root root  20 2022-04-13 19:38 resource -> /dev/block/mmcblk0p6
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 security -> /dev/block/mmcblk0p16
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 sw_release -> /dev/block/mmcblk0p26
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 system_a -> /dev/block/mmcblk0p18
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 system_b -> /dev/block/mmcblk0p19
lrwxrwxrwx 1 root root  20 2022-04-13 19:38 trust_a -> /dev/block/mmcblk0p3
lrwxrwxrwx 1 root root  20 2022-04-13 19:38 trust_b -> /dev/block/mmcblk0p4
lrwxrwxrwx 1 root root  20 2022-04-13 19:38 uboot_a -> /dev/block/mmcblk0p1
lrwxrwxrwx 1 root root  20 2022-04-13 19:38 uboot_b -> /dev/block/mmcblk0p2
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 userdata -> /dev/block/mmcblk0p28
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 vbmeta_a -> /dev/block/mmcblk0p11
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 vbmeta_b -> /dev/block/mmcblk0p12
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 vendor_a -> /dev/block/mmcblk0p21
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 vendor_b -> /dev/block/mmcblk0p22
lrwxrwxrwx 1 root root  21 2022-04-13 19:38 video -> /dev/block/mmcblk0p27
```


### Other ideas

Something that we can do is to unsolder the eMMC chip and read it externally so that we can dump all contents. It would be good to bake a CFW, but I'll not unsolder it from my ONLY Console (a spare one would be niiice).
