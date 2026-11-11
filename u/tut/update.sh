#!/bin/bash
# 퍼스널 OS 업데이트 — 설치 날 공식 실습(진행판·건너뛰기·완료 화면) 넣기 (2026-11-11)
set -e
O="$HOME/퍼스널OS"; K="$O/.os_키트"; B="https://mybrandium.com/u/tut"
[ -d "$K/_원본" ] || { echo "퍼스널 OS가 깔린 컴퓨터가 아니에요 (~/퍼스널OS 없음)"; exit 1; }
curl -fsSL "$B/tutorial.py" -o "$K/공식실습.py"
curl -fsSL "$B/complete.py" -o "$K/설치완료.py"
cp "$K/_원본/CLAUDE.md" "$K/_원본/CLAUDE.md.업데이트전_$(date +%y%m%d%H%M)"
curl -fsSL "$B/claude_tpl.md" -o "$K/_원본/CLAUDE.md"
python3 "$K/적용.py" >/dev/null
grep -q "공식실습.py" "$O/CLAUDE.md" && echo "✅ 업데이트 완료 — 매니저에게 '공식 실습 시작'이라고 말해 보세요."
