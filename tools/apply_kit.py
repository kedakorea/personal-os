#!/usr/bin/env python3
"""퍼스널 OS — 설정 적용 (설치 키트)

~/퍼스널OS/설정.json 의 매니저 이름·호칭·회사 등을 _원본 의 빈칸({{…}})에 채워 ~/퍼스널OS 에 깐다.
이름·호칭을 바꾸거나 부서표를 고친 뒤 다시 돌리면 된다. 대화·할일·메모 같은 자료는 건드리지 않는다.

    python3 ~/퍼스널OS/.os_키트/적용.py
"""
import json, os, re, shutil, sys

KIT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(KIT, "_원본")
OS_DIR = os.path.expanduser("~/퍼스널OS")
DATA = os.path.join(OS_DIR, ".os_데이터")
CONF = os.path.join(OS_DIR, "설정.json")
RECORD = os.path.join(DATA, "적용기록.json")

DEFAULT = {
    "실장": "매니저",
    "직함": "매니저",
    "호칭": "대표님",
    "회사": "",
    "앱이름": "",
    "비밀번호": "",
    "메일": "",
    "보안주소": "",
    "말투": "짧고 친절하게, 결론부터. 어려운 말은 쓰지 않는다.",
    "승인선": "- 메일 발송 · 결제 · 외부 게시 · 파일 삭제는 {{호칭}} 확인 후에만 한다.",
    "근무시간": "평일 09:30~18:30",
    "백업": "노션·옵시디언 백업은 세팅 뒤 연결한다.",
    "링크": [],
}

# 처음 한 번만 깔고, 그 뒤로는 이름·호칭만 바꿔 주는 파일 (안에 쌓인 내용을 지키려고)
ONCE = {"부서/부서표.json", "부서/00_비서실/CLAUDE.md", "부서/00_비서실/업무일지.md", "부서/00_비서실/추가지침.md"}
# 매번 새로 만드는 파일 — 손으로 고칠 내용은 부서/00_비서실/추가지침.md 에
ALWAYS_NOTE = {"CLAUDE.md": "<!-- 이 파일은 적용.py 가 설정.json 으로 만든다. 직접 고치지 말고 부서/00_비서실/추가지침.md 에 쓴다. -->\n"}


def load_conf():
    c = dict(DEFAULT)
    if os.path.exists(CONF):
        with open(CONF, encoding="utf-8") as f:
            c.update(json.load(f))
    else:
        os.makedirs(OS_DIR, exist_ok=True)
        with open(CONF, "w", encoding="utf-8") as f:
            json.dump(DEFAULT, f, ensure_ascii=False, indent=1)
    if not (c.get("실장") or "").strip():
        c["실장"] = c.get("직함") or "매니저"
    if not c.get("앱이름"):
        c["앱이름"] = c["실장"]
    return c


def dept_list():
    try:
        with open(os.path.join(OS_DIR, "부서", "부서표.json"), encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        try:
            with open(os.path.join(SRC, "부서", "부서표.json"), encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            return "- 00 비서실 — 퍼스널 OS 자체 관리"
    lines = ["| 부서 | 맡는 일 | 폴더 |", "|---|---|---|"]
    for x in d.get("부서", []):
        lines.append("| %s | %s | `부서/%s` |" % (x.get("이름") or x["폴더"].replace("_", " ", 1), x.get("일", "·".join(x.get("말", [])[:6])), x["폴더"]))
    return "\n".join(lines)


def values(c):
    links = [["os", "퍼스널 OS", "https://mybrandium.com/"]]
    for l in c.get("링크", []):
        if isinstance(l, (list, tuple)) and len(l) >= 2:
            links.append(["globe", l[0], l[1]])
    v = {k: (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) for k, v in c.items()}
    v["링크"] = json.dumps(links, ensure_ascii=False)
    v["부서목록"] = dept_list()
    v["회사"] = c.get("회사") or "우리 회사"
    return v


def fill(text, v):
    # 이름을 정하지 않았으면 실장 = 직함 — "비서실장 비서실장" 이 되지 않게 붙어 있는 자리를 하나로
    if v.get("실장") and v.get("실장") == v.get("직함"):
        text = text.replace("{{실장}} {{직함}}", "{{실장}}")
    # 받침에 맞게 조사 고르기 — "케니지이 답하는 중" → "케니지가 답하는 중" (2026-10-25 1호 설치 때 발견)
    def _josa(m):
        name = v.get(m.group(1), "")
        last = name.strip()[-1:] if name.strip() else ""
        batchim = bool(last) and "가" <= last <= "힣" and (ord(last) - 0xAC00) % 28 != 0
        pair = {"이": "가", "은": "는", "을": "를", "과": "와"}[m.group(2)]
        return "{{%s}}" % m.group(1) + (m.group(2) if batchim else pair)
    text = re.sub(r"\{\{(실장|호칭|회사)\}\}(이|은|을|과)(?=[\s.,…\"'<!?)·:]|$)", _josa, text)
    for _ in range(3):
        new = re.sub(r"\{\{([^{}]+)\}\}", lambda m: v.get(m.group(1), ""), text)
        if new == text:
            break
        text = new
    return text


def main():
    if not os.path.isdir(SRC):
        sys.exit("키트 원본이 없습니다: %s" % SRC)
    c = load_conf()
    v = values(c)
    os.makedirs(DATA, exist_ok=True)
    try:
        prev = json.load(open(RECORD, encoding="utf-8"))
    except Exception:
        prev = {}
    n = 0
    for root, dirs, files in os.walk(SRC):
        for f in files:
            if f == ".DS_Store":
                continue
            s = os.path.join(root, f)
            rel = os.path.relpath(s, SRC)
            d = os.path.join(OS_DIR, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            try:
                text = open(s, encoding="utf-8").read()
            except UnicodeDecodeError:
                shutil.copy2(s, d)
                continue
            if rel in ONCE and os.path.exists(d):
                # 이미 깔린 파일은 내용을 지키고 이름·호칭만 바꾼다
                t = open(d, encoding="utf-8").read()
                for k in ("실장", "호칭", "앱이름"):
                    if prev.get(k) and prev[k] != v[k]:
                        t = t.replace(prev[k], v[k])
                open(d, "w", encoding="utf-8").write(t)
                continue
            out = fill(text, v)
            if rel == "CLAUDE.md":
                extra = os.path.join(OS_DIR, "부서", "00_비서실", "추가지침.md")
                out = ALWAYS_NOTE[rel] + out
                if os.path.exists(extra):
                    out += "\n\n## 추가 지침\n" + open(extra, encoding="utf-8").read()
            if rel == "elvin_web.html":
                # 고객 맞춤 화면(사무실 등)은 부서/00_비서실/화면추가.html 에 둔다 → 다시 적용해도 사라지지 않는다 (2026-10-18 1호 때 사라짐)
                add = os.path.join(OS_DIR, "부서", "00_비서실", "화면추가.html")
                if os.path.exists(add):
                    i = out.rfind("</body>")
                    out = out[:i] + open(add, encoding="utf-8").read() + out[i:]
            with open(d, "w", encoding="utf-8") as fh:
                fh.write(out)
            if f.endswith((".sh", ".py", ".command")):
                os.chmod(d, 0o755)
            n += 1
    json.dump({k: v[k] for k in ("실장", "호칭", "앱이름")}, open(RECORD, "w", encoding="utf-8"), ensure_ascii=False)
    print("적용 완료 — %s · %s · 파일 %d개" % (v["실장"], v["호칭"], n))


if __name__ == "__main__":
    main()
