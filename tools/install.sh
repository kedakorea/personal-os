#!/bin/bash
# 퍼스널 OS 설치 시작 — 다운로드 폴더의 설치 키트를 찾아 '열지 않음' 경고 없이 바로 실행 (2026-10-18)
#   curl -fsSL https://kedakorea.github.io/personal-os/tools/install.sh | bash
D="$HOME/Downloads"
K=$(ls -dt "$D"/퍼스널OS_설치키트*/ 2>/dev/null | head -1)
if [ -z "$K" ]; then
  Z=$(ls -t "$D"/퍼스널OS_설치키트*.zip 2>/dev/null | head -1)
  [ -n "$Z" ] || { echo "다운로드 폴더에서 '퍼스널OS_설치키트' 를 못 찾았어요. 받은 키트를 다운로드 폴더에 두고 다시 실행해 주세요."; exit 1; }
  echo "압축 푸는 중…"; ditto -x -k "$Z" "$D" || { echo "압축을 풀지 못했어요"; exit 1; }
  K=$(ls -dt "$D"/퍼스널OS_설치키트*/ 2>/dev/null | head -1)
fi
K="${K%/}"
xattr -dr com.apple.quarantine "$K" 2>/dev/null          # 인터넷에서 받은 파일 표시 지우기 → '열지 않음' 안 뜸
python3 - "$K" <<'P'
import os, sys, unicodedata
for d, ds, fs in os.walk(sys.argv[1], topdown=False):      # 한글 파일 이름 바로잡기
    for f in fs + ds:
        g = unicodedata.normalize("NFC", f)
        if g != f:
            try: os.rename(os.path.join(d, f), os.path.join(d, g))
            except OSError: pass
P
chmod +x "$K"/*.command 2>/dev/null
echo "✓ 설치 키트 준비 완료: $K"
[ -n "$PERSONALOS_DRYRUN" ] && exit 0
exec bash "$K/설치.command"
