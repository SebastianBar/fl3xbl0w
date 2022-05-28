<p align="center">
  <img height="100" src="logo.png">
</p>

## fl3xbl0w

fl3xbl0w is an attempt to document as much as possible on the "Bowflex Console" (what Nautilus refers to as `Vantron`), which drives most of the "smart devices" from Bowflex (basically, an Android tablet running proprietary software).

This relies on some previous work provided over [Reddit](https://www.reddit.com/r/Bowflex/comments/mi8wdo/unlocking_bowflex_velocore/) (thanks [xasmx](https://www.reddit.com/user/xasmx/)!) to achieve a deeper understanding on the machine's software & hardware.


## Supported devices (Android Jailbreak)

After playing with the [decompiled apps](DECOMPILING.md) I can certainly say that the following documentation could be extrapolated in one way or another to the following Bowflex devices:

### Treadmills
- Treadmill 22 / Treadmill 56 (same treadmill. 56 is 220v AC input, 22 is 120v AC input)
- Treadmill 10 / Treadmill 25 (same treadmill. 25 is 220v AC input, 10 is 120v AC input)

### Bikes
- VeloCore

### Max Trainer
- Max Total 16
- Max Trainer M9

I don't own a Max Trainer or a VeloCore, but it should work as long as you have an available USB port based on the codebase findings.

Confirmed to be working with NautilusLauncher versions:
- 5.0.0.350
- 5.0.0.382 (latest as of May 2022)

> _Your device is supported but not on the list? Let us all know!_


## Documentation

### General information
- [Android Jailbreak](JAILBREAK.md)
- [Backup your Console contents](BACKUP.md)
- [Decompiling](DECOMPILING.md)
- [Bowflex Quirks](QUIRKS.md)

### Work in progress
- [Treadmill Motor Controller](MOTOR.md)
- [ROM Dump](ROMDUMP.md)

## End goal

To enable as much future-proofing to my treadmill as possible.

Nautilus, Inc. only provides a 1-year warranty on the electronics side of things, and as soon as I saw that the mechanism for turning off the machine (and so, the Android tablet) was to basically "cut the AC power through the back switch", that scared me. Every Linux-based device should be safely turned off to avoid OS corruption, and this Android tablet is no exception. So while it's working, why not have some "extra fun" with it?.

In the end, I want to intercept, understand, and recreate the communication going to the Motor Control Board on my treadmill so if the tablet dies, I still have a working device.

**This is not for sharing copyrighted software.**