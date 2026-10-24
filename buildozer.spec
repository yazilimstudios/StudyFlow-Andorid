[app]
title = StudyFlow
package.name = studyflow
package.domain = org.efe
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,flet
orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# Sabit ve sorunsuz sürümler:
android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.0

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
