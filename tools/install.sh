#!/bin/bash
# 퍼스널 OS 설치 시작 — 다운로드 폴더의 설치 키트를 찾아 '열지 않음' 경고 없이 바로 실행 (2026-10-18)
#   curl -fsSL https://kedakorea.github.io/personal-os/tools/install.sh | bash
D="$HOME/Downloads"
# 이사(2026-10-19) — 옛 컴퓨터에서 만든 '퍼스널OS_이사짐_날짜.zip' 이 있으면 그대로 풀어 이어서 설치한다
M=$(ls -t "$D"/퍼스널OS_이사짐_*.zip "$HOME/Desktop"/퍼스널OS_이사짐_*.zip 2>/dev/null | head -1)
if [ -n "$M" ] && [ ! -d "$HOME/퍼스널OS" ]; then
  echo "📦 이사짐을 찾았어요: $(basename "$M") — 푸는 중…"
  ditto -x -k "$M" "$HOME" || { echo "이사짐을 풀지 못했어요"; exit 1; }
  xattr -dr com.apple.quarantine "$HOME/퍼스널OS" 2>/dev/null
  python3 - "$HOME/퍼스널OS" <<'Q'
import os, sys, unicodedata
for d, ds, fs in os.walk(sys.argv[1], topdown=False):
    for f in fs + ds:
        g = unicodedata.normalize("NFC", f)
        if g != f:
            try: os.rename(os.path.join(d, f), os.path.join(d, g))
            except OSError: pass
Q
  chmod +x "$HOME/퍼스널OS"/*.command "$HOME/퍼스널OS/.os_키트"/*.py 2>/dev/null
  echo "✓ 옛 컴퓨터의 설정·부서·기록을 그대로 가져왔어요. 이어서 이 컴퓨터에 설치합니다."
  [ -n "$PERSONALOS_DRYRUN" ] && exit 0
  if ! xcode-select -p >/dev/null 2>&1; then
    echo "먼저 맥 기본 개발 도구가 필요해요. 뜨는 창에서 [설치]를 누르고, 끝나면 이 한 줄을 다시 실행해 주세요."
    xcode-select --install 2>/dev/null; exit 0
  fi
  exec /usr/bin/python3 "$HOME/퍼스널OS/.os_키트/설치기.py"
fi
K=$(ls -dt "$D"/퍼스널OS_설치키트*/ 2>/dev/null | head -1)
if [ -z "$K" ]; then
  Z=$(ls -t "$D"/퍼스널OS_설치키트*.zip "$D"/PersonalOS_Kit*.zip 2>/dev/null | head -1)   # 고객 페이지에서 받은 키트는 PersonalOS_Kit_날짜.zip (2026-10-19)
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
