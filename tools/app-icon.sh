#!/bin/bash
# 퍼스널 OS — 바탕화면·Dock 에 앱 아이콘 만들기 (설치기 6-2 단계와 같음, 2026-10-18)
APP="$HOME/Applications/퍼스널 OS.app"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cat > "$APP/Contents/MacOS/run" <<'R'
#!/bin/bash
URL=http://127.0.0.1:8765
if [ -d "/Applications/Google Chrome.app" ]; then open -na "Google Chrome" --args --app="$URL" --start-maximized; else open "$URL"; fi
R
chmod +x "$APP/Contents/MacOS/run"
cat > "$APP/Contents/Info.plist" <<'P'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict><key>CFBundleName</key><string>퍼스널 OS</string><key>CFBundleIdentifier</key><string>com.personalos.app</string><key>CFBundleExecutable</key><string>run</string><key>CFBundleIconFile</key><string>icon</string><key>CFBundlePackageType</key><string>APPL</string></dict></plist>
P
PNG="$HOME/퍼스널OS/os_아이콘.png"
if [ -f "$PNG" ]; then
  T=$(mktemp -d)/icon.iconset; mkdir -p "$T"
  for s in 16 32 128 256 512; do sips -z $s $s "$PNG" --out "$T/icon_${s}x${s}.png" >/dev/null; d=$((s*2)); sips -z $d $d "$PNG" --out "$T/icon_${s}x${s}@2x.png" >/dev/null; done
  iconutil -c icns "$T" -o "$APP/Contents/Resources/icon.icns"
fi
xattr -dr com.apple.quarantine "$APP" 2>/dev/null
[ -e "$HOME/Desktop/퍼스널 OS" ] || ln -s "$APP" "$HOME/Desktop/퍼스널 OS"
if ! defaults read com.apple.dock persistent-apps 2>/dev/null | grep -q "com.personalos\|%ED%8D%BC%EC%8A%A4%EB%84%90"; then
  defaults write com.apple.dock persistent-apps -array-add "<dict><key>tile-data</key><dict><key>file-data</key><dict><key>_CFURLString</key><string>$APP</string><key>_CFURLStringType</key><integer>0</integer></dict></dict></dict>"
  killall Dock
fi
echo "✓ 바탕화면·Dock 에 '퍼스널 OS' 아이콘을 만들었습니다."
open "$APP"
