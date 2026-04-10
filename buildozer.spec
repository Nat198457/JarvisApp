
[app]

; (str) Title of your application
title = Jarvis

; (str) Package name
package.name = jarvis

; (str) Package domain - cambia 'tu.nombre' por lo que quieras
package.domain = org.jarvis.v29

; (str) Source code where your app.py is located
source.dir =.

; (list) Source files to include
source.include_exts = py

; (str) Application version
version = 2.9

; (list) Requirements for your app
requirements = python3,kivy,pyjnius,speechrecognition,pyttsx3,requests,cryptography

; (list) Permissions needed
android.permissions = RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,WAKE_LOCK,INTERNET

; (str) Orientation
orientation = portrait

; (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

; (list) List of service to launch
services =

; (str) Android API to use
android.api = 33

; (str) Minimum API your APK will support
android.minapi = 21

; (str) Android NDK version
android.ndk = 25b

; (bool) Use --private storage
android.private_storage = True

; (str) Android entry point
android.entrypoint = org.kivy.android.PythonService

; (str) Android app theme
android.theme = @android:style/Theme.NoTitleBar

; (list) Android whitelist
android.whitelist =

; (str) Android architecture
android.archs
