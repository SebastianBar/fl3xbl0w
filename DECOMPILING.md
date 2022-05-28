<p align="center">
  <img height="100" src="logo.png">
</p>

## Decompiling | fl3xbl0w

This assumes you already [have your own APKs](BACKUP.md). Note that even though I'm specifying this on Nautilus' apps, this applies to pretty much any Android application you'd like to "peek under the hood".


## Turning apps into Java code

The following instructions are intended to get some "readable code", but it's improbable that you'll be able to compile them back to an APK. I'm using this as a reference to understand Nautilus' developers. If you want to alter the codebase and package it back, go to [Turning apps into Smali code](#turning-apps-into-smali-code).

### Requirements
- [jadx](https://github.com/skylot/jadx)


### Let's open some sh*t

After installing `jadx` you should be able to open `jadx-gui`. Go to File -> Open files ...
![jadx-gui screen](/assets/screen-jadx-init.png) 

Search for your desired APK and click on "Open file":
![jadx-gui selecting apk](/assets/screen-jadx-open.png) 

And from there, you can start poking around:
![jadx-gui decompiling NautilusLauncher](/assets/screen-jadx-opened.png "onStartCommand blah blah?") 

If you want to save the project as Java files, go into File -> Save as gradle project:
![jadx-gui saving project](/assets/screen-jadx-save.png) 

If useful, here are my `jadx-gui` preferences:
![jadx-gui preferences](/assets/screen-jadx-preferences.png) 


## Turning apps into Smali code

The community has tested this to apply some patches to our APKs. It would only work for non-system apps, as without the proper signing key, the app will not have access to system resources (such as the Serial port).

https://www.reddit.com/r/Bowflex/comments/mi8wdo/unlocking_bowflex_velocore/