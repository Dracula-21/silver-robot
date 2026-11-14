[app]
title = PhoneChecker
package.name = phonechecker
package.domain = org.test
source.dir = .
version = 0.1
requirements = python3,kivy,telethon,pyaes,rsa,pyasn1,sqlite3
source.include_patterns = session.session
android.permissions = INTERNET
android.archs = arm64-v8a
android.accept_sdk_license = True
android.api = 33
android.ndk = 25b
orientation = portrait

[buildozer]
log_level = 2
