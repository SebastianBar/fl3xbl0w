import sys
import os
import subprocess
from datetime import datetime

# check if argument is given
if len(sys.argv) != 2:
    print("Usage: python3 dump.py <Console IP Address>")
    sys.exit(1)

ipaddr = sys.argv[1]

# check if adb is available for shell
adb_path = subprocess.check_output(["which", "adb"]).decode("utf-8").strip()
if not os.path.exists(adb_path):
    print("adb not found")
    exit()

# setup dump folder with current date and time
dump_folder = os.path.join(
    os.environ["HOME"],
    "Desktop",
    "nautilus_dump",
    "{}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")),
)
if not os.path.exists(dump_folder):
    os.makedirs(dump_folder)

# connect adb
print("Connecting to {}...".format(ipaddr))
subprocess.call(["adb connect {}".format(ipaddr)], shell=True)

# pull /sdcard contents
print("Pulling /sdcard contents...")
subprocess.call(["adb pull /sdcard/ {}".format(dump_folder)], shell=True)

# get APK info
print("Pulling APKs...")
packages = (
    subprocess.check_output(["adb shell pm list packages -f"], shell=True)
    .decode("utf-8")
    .split("\n")
)

# filter out empty lines
packages = [x for x in packages if x.strip()]

# filter out lines containing "com.android", "com.google", "framework-res"
packages = [package for package in packages if package.find("com.android") == -1]
packages = [package for package in packages if package.find("com.google") == -1]
packages = [package for package in packages if package.find("framework-res") == -1]

print("Found {} APKs".format(len(packages)))

for package in packages:
    package_name = package.split("=")
    package_name = package_name[len(package_name) - 1].strip()
    package_version = (
        subprocess.check_output(
            ["adb shell dumpsys package {} | grep versionName".format(package_name)],
            shell=True,
        )
        .decode("utf-8")
        .split("=")[1]
        .strip()
    )

    package_path = package.split(":")[1].split(".apk=")[0].strip()
    package_path = "{}.apk".format(package_path)
    print("Pulling {} v{}...".format(package_name, package_version))

    subprocess.call(["adb pull {} {}".format(package_path, dump_folder)], shell=True)

    os.rename(
        os.path.join(dump_folder, os.path.basename(package_path)),
        os.path.join(dump_folder, "{}-{}.apk".format(package_name, package_version)),
    )

# backup appdata
print("Backing up appdata.adb ...")
print('TOUCH THE "BACK UP MY DATA" BUTTON ON SCREEN NOW !!!')
subprocess.call(
    ["adb backup -f {}/appdata.adb -all -noapk -nosystem".format(dump_folder)],
    shell=True,
)

# disconnect adb
print("Disconnecting...")
subprocess.check_output(["adb disconnect"], shell=True)
