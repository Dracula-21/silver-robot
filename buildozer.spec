[app]
title = PhoneChecker
package.name = phonechecker
package.domain = org.test
source.dir = .
version = 0.1
# Жестко фиксируем версию Cython и Kivy
requirements = python3,cython==0.29.36,kivy,telethon,pyaes,rsa,pycryptodomex
android.archs = arm64-v8a
android.accept_sdk_license = True
android.api = 33
android.ndk = 25b
orientation = portrait

[buildozer]
log_level = 2
