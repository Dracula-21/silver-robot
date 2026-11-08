[app]
title = PhoneChecker
package.name = phonechecker
package.domain = org.test
source.dir = .
version = 0.1
requirements = python3,kivy,telethon
android.archs = arm64-v8a
android.accept_sdk_license = True
android.api = 33
android.ndk = 25b
# Фиксируем стабильную версию python-for-android, которая совместима с Kivy и Cython < 3.0
p4a.branch = v2023.09.18

[buildozer]
log_level = 2
