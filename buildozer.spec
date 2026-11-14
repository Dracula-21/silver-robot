[app]
title = PhoneChecker
package.name = phonechecker
package.domain = org.test
source.dir = .
version = 0.1
requirements = python3,kivy,telethon

# Явно указываем пути к инструментам
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

android.archs = arm64-v8a
android.accept_sdk_license = True
android.api = 33
android.ndk = 25b
p4a.branch = master

[buildozer]
log_level = 2
