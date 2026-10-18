#!/bin/bash
# 조연심 대표 퍼스널 OS — 사무실 화면 넣기 (2026-10-18)
# 지금 앱 파일과 '원본 틀' 둘 다 고친다 → 설정을 다시 적용(적용.py)해도 사무실 화면이 사라지지 않는다
OS="$HOME/퍼스널OS"
[ -f "$OS/elvin_web.html" ] || { echo "퍼스널 OS 앱 파일을 못 찾았어요 ($OS/elvin_web.html)"; exit 1; }
curl -fsSL "https://kedakorea.github.io/personal-os/tools/office-jys.html?$(date +%s)" -o /tmp/office-jys.html || { echo "내려받기 실패 — 인터넷 연결을 확인해 주세요"; exit 1; }
for F in "$OS/elvin_web.html" "$OS/.os_키트/_원본/elvin_web.html"; do
  [ -f "$F" ] || continue
  [ -f "$F.사무실전_백업" ] || cp "$F" "$F.사무실전_백업"
  python3 - "$F" /tmp/office-jys.html <<'P'
import sys, re
f, o = sys.argv[1], sys.argv[2]
s = open(f, encoding="utf-8").read(); add = open(o, encoding="utf-8").read()
s = re.sub(r"<!--OFFICE-START.*?<!--OFFICE-END-->\n?", "", s, flags=re.S)
ra = s.find("<!-- ═══ 레트로 데스크톱 화면")          # 레트로(조사병단 본부·창 모드) 코드 삭제
if ra >= 0:
    rb = s.find("<script>\n(function () {", ra); re_ = s.find("\n})();\n</script>", rb)
    if rb >= 0 and re_ >= 0:
        s = s[:ra] + s[re_ + len("\n})();\n</script>"):]
i = s.rfind("</body>"); s = s[:i] + add + s[i:]
open(f, "w", encoding="utf-8").write(s)
P
done
echo "✓ 사무실 화면을 넣었습니다 (원본 틀까지 — 설정을 다시 적용해도 유지). 앱 창에서 새로고침(⌘R) 하세요."
