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
# 새 판 적용.py 는 부서/00_비서실/화면추가.html 을 알아서 다시 붙인다 — 같이 넣어 둔다
mkdir -p "$OS/부서/00_비서실" && cp /tmp/office-jys.html "$OS/부서/00_비서실/화면추가.html"
# 매니저 이름을 '찰스 핸디'로 (비어 있을 때만) → 원본 틀로 다시 깔기(사무실 화면 포함)
python3 - "$OS/설정.json" <<'P'
import sys, json
p = sys.argv[1]
try:
    c = json.load(open(p, encoding="utf-8"))
except Exception:
    sys.exit(0)
if not (c.get("실장") or "").strip() or c.get("실장") == c.get("직함"):
    c["실장"] = "찰스 핸디"; c.setdefault("직함", "실장")
    json.dump(c, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
P
[ -f "$OS/.os_키트/적용.py" ] && python3 "$OS/.os_키트/적용.py" >/dev/null 2>&1
echo "✓ 사무실 화면을 넣었습니다 (원본 틀까지 — 설정을 다시 적용해도 유지). 앱 창에서 새로고침(⌘R) 하세요."
