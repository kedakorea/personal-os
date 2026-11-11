#!/usr/bin/env python3
"""설치 날 공식 실습(튜토리얼) 진행판 — 실습 2가지(2026-11-11 대표님: 3→2, 콘텐츠 올리기는 공식 뒤 자유)를 하나씩 체크하고, 다 끝나면(또는 건너뛰면) 설치 완료 화면으로 (2026-11-11 대표님 지시)
사용:
  python3 공식실습.py start            # 진행판을 처음부터 띄운다
  python3 공식실습.py done 1           # 1번 실습 완료
  python3 공식실습.py skip 2 "사유"    # 2번 건너뜀 (채널 계정을 못 찾았을 때 등) — 완료 화면에 '다음에 해 보기'로 남는다
  python3 공식실습.py show             # 진행판만 다시 띄운다
- 화면: ~/퍼스널OS/결과물/공식실습.html (3초마다 저절로 새로 고침)
- 두 가지가 모두 완료·건너뜀이 되면 설치완료.py 를 저절로 부른다(한 번만)
"""
import html, json, os, subprocess, sys, time, webbrowser

OS_DIR = os.path.expanduser("~/퍼스널OS")
KIT = os.path.join(OS_DIR, ".os_키트")
ST = os.path.join(OS_DIR, ".os_데이터", "공식실습.json")
OUT_DIR = os.path.join(OS_DIR, "결과물")
OUT = os.path.join(OUT_DIR, "공식실습.html")
E = html.escape
try:
    c = json.load(open(os.path.join(OS_DIR, "설정.json"), encoding="utf-8"))
except Exception:
    c = {}
MGR, CALL = c.get("실장") or "매니저", c.get("호칭") or "대표님"
STEPS = [
    ("콘텐츠 만들기", "설치 기념 카드뉴스 + 숏폼 영상", "설치 기념 카드뉴스 만들어 줘"),
    ("휴대폰으로 일 맡기기", "밖에서 휴대폰으로 시키고 알림 받기", "(휴대폰 앱에서) 가장 귀찮은 일 하나 맡기기"),
]


def load():
    try:
        return json.load(open(ST, encoding="utf-8"))
    except Exception:
        return {"시작": "", "단계": [{"상태": "대기", "사유": "", "시각": ""} for _ in STEPS], "완료화면": False}


def save(s):
    os.makedirs(os.path.dirname(ST), exist_ok=True)
    json.dump(s, open(ST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def page(s):
    st = s["단계"]
    closed = sum(1 for x in st if x["상태"] in ("완료", "건너뜀"))
    cur = next((i for i, x in enumerate(st) if x["상태"] == "대기"), None)
    cards = ""
    for i, (t, d, say) in enumerate(STEPS):
        x = st[i]
        if x["상태"] == "완료":
            cls, mark, tail = "ok", "✓", f"완료 · {E(x['시각'])}"
        elif x["상태"] == "건너뜀":
            cls, mark, tail = "sk", "↷", "건너뜀 — 나중에 언제든 해 볼 수 있어요" + (f" ({E(x['사유'])})" if x["사유"] else "")
        elif i == cur:
            cls, mark, tail = "now", str(i + 1), f"지금 하는 중 · 이렇게 말해 보세요 <b>“{E(say)}”</b>"
        else:
            cls, mark, tail = "wait", str(i + 1), "다음 차례"
        if i == 1 and x["상태"] == "대기":
            tail += ' · <a href="휴대폰연결.html" target="_blank" style="font-weight:800;color:#2f7fe6">📱 휴대폰 연결 화면(QR) 열기</a>'
        cards += f'<div class="st {cls}"><span>{mark}</span><div><b>실습 {i + 1} · {E(t)}</b><small>{E(d)}</small><em>{tail}</em></div></div>'
    done_all = closed == len(STEPS)
    head = "🎉 공식 실습 끝! 완료 화면으로 넘어가요" if done_all else f"공식 실습 {closed} / {len(STEPS)}"
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="3"><title>공식 실습 — 퍼스널 OS</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Pretendard,-apple-system,'Malgun Gothic',sans-serif;background:#faf9f6;color:#1c1c1e;word-break:keep-all}}
.w{{max-width:760px;margin:0 auto;padding:44px 22px}}.k{{font-weight:800;color:#2f9a6a;font-size:16px;letter-spacing:2px}}
h1{{font-size:38px;line-height:1.25;margin:10px 0 8px}}p.l{{font-size:18px;color:#555;line-height:1.6}}
.bar{{height:14px;background:#e7e5df;border-radius:99px;margin:24px 0 20px;overflow:hidden}}.bar i{{display:block;height:100%;background:#2f9a6a;width:{closed / len(STEPS) * 100:.0f}%;transition:width .4s}}
.st{{display:flex;gap:16px;align-items:center;background:#fff;border:2px solid #e3e1da;border-radius:20px;padding:20px 22px;margin-bottom:12px}}
.st span{{flex:0 0 52px;height:52px;border-radius:16px;background:#e7e5df;color:#777;display:flex;align-items:center;justify-content:center;font:900 24px Pretendard}}
.st b{{display:block;font-size:21px}}.st small{{display:block;font-size:15.5px;color:#666;margin-top:3px}}.st em{{display:block;font-style:normal;font-size:16px;margin-top:8px;color:#777}}
.st.now{{border-color:#1c1c1e;box-shadow:0 8px 24px rgba(0,0,0,.08)}}.st.now span{{background:#1c1c1e;color:#fff}}.st.now em{{color:#1c1c1e}}
.st.ok span{{background:#2f9a6a;color:#fff}}.st.ok em{{color:#2f9a6a;font-weight:700}}.st.sk{{opacity:.75}}.st.sk span{{background:#c9c6bd;color:#fff}}
.f{{margin-top:18px;font-size:15px;color:#777;line-height:1.6}}</style></head><body><div class="w">
<div class="k">OFFICIAL TUTORIAL</div><h1>{E(head)}</h1>
<p class="l">설치가 끝났어요. 이제 {E(MGR)}{E('과' if (MGR and '가' <= MGR[-1] <= '힣' and (ord(MGR[-1]) - 0xAC00) % 28) else '와')} 실습 2가지만 해 보면 오늘 설치는 공식적으로 끝나요.</p>
<div class="bar"><i></i></div>{cards}
<p class="f">계정이 없거나 오늘 하기 어려운 실습은 건너뛰어도 괜찮아요. 완료 화면에 '다음에 해 보기'로 남겨 둘게요.</p>
</div></body></html>"""


def render(s, open_it=False):
    os.makedirs(OUT_DIR, exist_ok=True)
    try:
        subprocess.run([sys.executable, os.path.join(KIT, "휴대폰연결안내.py"), "--no-open"], capture_output=True, timeout=20)
    except Exception:
        pass
    open(OUT, "w", encoding="utf-8").write(page(s))
    if open_it:
        webbrowser.open("file://" + OUT)


def maybe_finish(s):
    if s.get("완료화면") or any(x["상태"] == "대기" for x in s["단계"]):
        return
    s["완료화면"] = True
    save(s)
    time.sleep(3)
    subprocess.run([sys.executable, os.path.join(KIT, "설치완료.py")])


def main():
    a = sys.argv[1:] or ["show"]
    s = load()
    if a[0] == "start":
        s = {"시작": time.strftime("%Y-%m-%d %H:%M"), "단계": [{"상태": "대기", "사유": "", "시각": ""} for _ in STEPS], "완료화면": False}
        save(s); render(s, True); print("공식 실습 진행판을 띄웠어요:", OUT); return
    if a[0] in ("done", "skip") and len(a) >= 2 and a[1].isdigit() and 1 <= int(a[1]) <= len(STEPS):
        x = s["단계"][int(a[1]) - 1]
        x["상태"] = "완료" if a[0] == "done" else "건너뜀"
        x["사유"] = " ".join(a[2:]) if a[0] == "skip" else ""
        x["시각"] = time.strftime("%H:%M")
        save(s); render(s)
        print(f"실습 {a[1]} {x['상태']}")
        maybe_finish(s); return
    render(s, True); print("진행판:", OUT)


if __name__ == "__main__":
    main()
