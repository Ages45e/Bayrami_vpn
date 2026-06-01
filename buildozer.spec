[app]
title = Bayrami VPN Pro
package.name = bayramivpnpro
package.domain = com.bayrami
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 4.0.0
requirements = python3,kivy==2.1.0,requests,urllib3
orientation = portrait
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 23b
android.sdk = 31
android.arch = arm64-v8a

[buildozer]
log_level = 2
