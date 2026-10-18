#!/bin/bash
# 조연심 대표 퍼스널 OS — 첫 화면에 '사무실'(찰스 실장 + 멘토 직원 10명) 넣기 (2026-10-18)
F="$HOME/퍼스널OS/elvin_web.html"
[ -f "$F" ] || { echo "퍼스널 OS 앱 파일을 못 찾았어요 ($F)"; exit 1; }
cp "$F" "$F.사무실전_백업"
curl -fsSL "https://kedakorea.github.io/personal-os/tools/office-jys.html?$(date +%s)" -o /tmp/office-jys.html || { echo "내려받기 실패 — 인터넷 연결을 확인해 주세요"; exit 1; }
python3 - "$F" /tmp/office-jys.html <<'P'
import sys, re
f, o = sys.argv[1], sys.argv[2]
s = open(f, encoding="utf-8").read(); add = open(o, encoding="utf-8").read()
s = re.sub(r"<!--OFFICE-START.*?<!--OFFICE-END-->\n?", "", s, flags=re.S)
i = s.rfind("</body>"); s = s[:i] + add + s[i:]
open(f, "w", encoding="utf-8").write(s)
P
echo "✓ 사무실 화면을 넣었습니다. 퍼스널 OS 앱 창에서 새로고침(⌘R) 하세요."
