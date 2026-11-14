winget install --id Google.AndroidCLI -e --silent --accept-package-agreements --accept-source-agreements
winget install --id Google.PlatformTools -e --silent --accept-package-agreements --accept-source-agreements

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$sdkDir = "$env:LOCALAPPDATA\Android\Sdk"
New-Item -ItemType Directory -Path $sdkDir -Force | Out-Null

android sdk install --sdk="$sdkDir" "cmdline-tools;latest" "platform-tools" "emulator" "system-images;android-30;google_apis_playstore;x86_64"

$avdRoot = "$env:USERPROFILE\.android\avd"
$avdDir = "$avdRoot\Moinul_Lite_GMS.avd"
New-Item -ItemType Directory -Path $avdDir -Force | Out-Null

@"
avd.ini.encoding=UTF-8
path=$avdDir
path.rel=avd\Moinul_Lite_GMS.avd
target=android-30
"@ | Out-File -FilePath "$avdRoot\Moinul_Lite_GMS.ini" -Encoding ascii

@"
AvdId=Moinul_Lite_GMS
PlayStore.enabled=true
abi.type=x86_64
avd.ini.displayname=Moinul_Lite_GMS
avd.ini.encoding=UTF-8
disk.dataPartition.size=4096M
hw.cpu.arch=x86_64
hw.cpu.ncore=2
hw.device.name=pixel_4
hw.gpu.enabled=yes
hw.gpu.mode=swiftshader_indirect
hw.keyboard=yes
hw.lcd.density=320
hw.lcd.height=1280
hw.lcd.width=720
hw.ramSize=2048
image.sysdir.1=system-images\android-30\google_apis_playstore\x86_64\
tag.display=Google Play
tag.id=google_apis_playstore
"@ | Out-File -FilePath "$avdDir\config.ini" -Encoding ascii

Write-Host "Setup Complete! Run: python android_emu_manager.py" -ForegroundColor Green
