
[app]
title = Jarvis
package.name = jarvis
package.domain = org.nat
source.dir =.
source.include_exts = py,kv,png,jpg
version = 2.9
requirements = python3,kivy,pyjnius,speechrecognition
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[android]
android.permissions = RECORD_AUDIO,INTERNET
android.api = 31
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
