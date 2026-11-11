#!/usr/bin/env python3
"""오늘 설치 공식 완료 — 공식 실습 3가지가 끝나면 고객 화면에 완료 안내를 띄운다 (2026-11-07 대표님 지시)
사용: python3 설치완료.py
- 결과물/설치완료.html 을 만들어 브라우저로 띄운다(축하 · 오늘 한 것 · 내 사용 가이드 · 30일 지원 · 문의처)
- 휴대폰 알림 한 번, 메모판에 '설치 완료 안내' 한 장, 업무일지 한 줄
- 다시 불러도 된다(같은 날이면 덮어씀)
"""
import html, json, os, platform, subprocess, time, webbrowser

OS_DIR = os.path.expanduser("~/퍼스널OS")
c = json.load(open(os.path.join(OS_DIR, "설정.json"), encoding="utf-8"))
MGR, CALL, CO = c.get("실장") or "매니저", c.get("호칭") or "대표님", c.get("회사") or ""
GUIDE = c.get("가이드") or "https://mybrandium.com"
KAKAO = "https://pf.kakao.com/_gMxogd"
ds = []
try:
    ds = [d["이름"].split(" ", 1)[-1] for d in json.load(open(os.path.join(OS_DIR, "부서", "부서표.json"), encoding="utf-8"))["부서"] if not d["폴더"].startswith("00")]
except Exception:
    pass
TODAY = time.strftime("%Y.%m.%d")
# 공식 실습 진행판(공식실습.py) 결과 — 건너뛴 실습은 '다음에 해 보기'로 보여 준다
STEPS = [("연결하기 — 지메일·드라이브·캘린더·노션", "연결했어"), ("나를 알아보는지 확인 — 매니저가 나를 소개", "내가 누군지 설명해 봐"), ("화면 바꿔 보기 — 말 한마디로 내 화면 고치기", "화면에서 ○○ 바꿔 줘")]
try:
    ST = json.load(open(os.path.join(OS_DIR, ".os_데이터", "공식실습.json"), encoding="utf-8"))["단계"]
except Exception:
    ST = [{"상태": "완료"}] * len(STEPS)
DONE_HTML = "".join((f'<div><span>✓</span>{"①②③"[i]} {html.escape(t)}</div>' if ST[i].get("상태") != "건너뜀" else f'<div class="sk"><span>↷</span><p>{"①②③"[i]} {html.escape(t)}<small>다음에 해 보기 — 언제든 “{html.escape(say)}”라고 말씀하시면 돼요</small></p></div>') for i, (t, say) in enumerate(STEPS))
N_DONE = sum(1 for x in ST if x.get("상태") != "건너뜀")
SUPPORT_END = time.strftime("%Y.%m.%d", time.localtime(time.time() + 30 * 86400))
E = html.escape


def josa(w, a, b):
    """받침 있으면 a(과·이), 없으면 b(와·가)"""
    ch = (w or " ")[-1]
    return w + (a if "가" <= ch <= "힣" and (ord(ch) - 0xAC00) % 28 else b)

page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>설치 완료 — 퍼스널 OS</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Pretendard,-apple-system,'Malgun Gothic',sans-serif;background:#faf9f6;color:#1c1c1e;word-break:keep-all}}
.w{{max-width:720px;margin:0 auto;padding:48px 22px 60px}}
.badge{{display:inline-block;background:#2f9a6a;color:#fff;font-weight:800;border-radius:99px;padding:8px 16px;font-size:15px}}
h1{{font-size:40px;line-height:1.25;margin:18px 0 10px}}p.lead{{font-size:19px;line-height:1.6;color:#555}}
.done{{margin:28px 0;display:grid;gap:12px}}
.done div{{background:#fff;border:2px solid #e3e1da;border-radius:18px;padding:18px 20px;display:flex;gap:14px;align-items:center;font-size:18px;font-weight:700}}
.done span{{flex:0 0 40px;height:40px;border-radius:12px;background:#2f9a6a;color:#fff;display:flex;align-items:center;justify-content:center;font-size:22px}}
.card{{background:#fff;border:2px solid #1c1c1e;border-radius:20px;padding:22px;margin-top:16px}}
.card h2{{font-size:20px;margin-bottom:10px}}.card li{{margin:8px 0 0 20px;font-size:16.5px;line-height:1.6}}
.btns{{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}}
a.b{{display:inline-block;text-decoration:none;font-weight:800;font-size:16px;border-radius:99px;padding:13px 20px;border:2px solid #1c1c1e;color:#1c1c1e;background:#fff}}
a.b.p{{background:#1c1c1e;color:#fff}}
.hero{{background:#1c1c1e;color:#fff;border-radius:26px;padding:40px 24px;text-align:center;margin-bottom:26px;animation:pop .7s cubic-bezier(.2,1.6,.4,1)}}.hero .big{{font:900 64px/1 Pretendard,sans-serif;letter-spacing:2px;color:#ffd84d}}.hero .sm{{margin-top:12px;font-size:17px;font-weight:700;opacity:.85}}
@keyframes pop{{from{{transform:scale(.6);opacity:0}}to{{transform:scale(1);opacity:1}}}}
.done div.sk{{opacity:.8;border-style:dashed}}.done div.sk span{{background:#c9c6bd}}.done p small{{display:block;font-size:14.5px;font-weight:600;color:#777;margin-top:4px}}
.conf{{position:fixed;inset:0;pointer-events:none;overflow:hidden}}.conf i{{position:absolute;top:-20px;width:10px;height:16px;border-radius:3px;animation:f 3.2s ease-in forwards}}
@keyframes f{{to{{transform:translateY(110vh) rotate(540deg)}}}}
</style></head><body><div class="conf" id="cf"></div><div class="w">
<div class="hero"><div class="big">COMPLETE!</div><div class="sm">퍼스널 OS 설치 완료 · 공식 설치 서비스 종료 · {TODAY}</div></div>
<span class="badge">🎉 공식 실습 {N_DONE} / {len(STEPS)} 완료</span>
<h1>{E(CALL)}, 고생하셨습니다!<br>오늘 설치는 공식적으로 완료되었습니다.</h1>
<p class="lead" style="font-weight:800;color:#2f9a6a">✔ 오늘 공식 설치 서비스는 여기서 끝났습니다. 이제부터는 자유롭게 써 보세요.</p>
<p class="lead">{E(CO + ' ' if CO else '')}퍼스널 OS가 오늘부터 출근합니다. {('매니저 <b>' + E(MGR) + '</b>' + josa('', '과', '와')[:0] + ('과 ' if (ord(MGR[-1]) - 0xAC00) % 28 and '가' <= MGR[-1] <= '힣' else '와 ') + E(josa(' · '.join(ds), '이', '가'))) if ds else ('매니저 <b>' + E(josa(MGR, '이', '가')) + '</b>')} {E(CALL)}의 일을 기다리고 있어요.</p>
<div class="done">{DONE_HTML}</div>
<div class="card"><h2>내일부터는 이렇게</h2><ul>
 <li>아침에 앱을 열고 <b>"브리핑"</b> 한마디로 하루를 시작하세요.</li>
 <li>일이 생기면 {E(MGR)}에게 그냥 말하듯 맡기면 됩니다. 컴퓨터는 켜 두세요(꺼지면 퇴근).</li>
 <li>메일은 임시보관함까지만 만들어 둡니다. 보내기는 직접 눌러 주세요.</li>
</ul></div>
<div class="card"><h2>도움이 필요할 때</h2><ul>
 <li><b>30일 지원</b> — {SUPPORT_END}까지 무엇이든 물어보세요.</li>
 <li>앱에서 "가이드 보여 줘"라고 하면 사용 가이드가 열려요.</li>
</ul>
<div class="btns"><a class="b p" href="{E(GUIDE)}" target="_blank">📘 내 사용 가이드</a><a class="b" href="{KAKAO}" target="_blank">💬 브랜디움 카카오 채널</a></div></div>
</div><script>
const C=['#2f9a6a','#ffd84d','#ff8a80','#7cb8ff','#c9a7ff'];const cf=document.getElementById('cf');
for(let i=0;i<90;i++){{const e=document.createElement('i');e.style.left=Math.random()*100+'vw';e.style.background=C[i%5];e.style.animationDelay=Math.random()*1.2+'s';cf.appendChild(e);}}
</script></body></html>"""

out_dir = os.path.join(OS_DIR, "결과물"); os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "설치완료.html")
open(out, "w", encoding="utf-8").write(page)
webbrowser.open("file://" + out)


def run(cmd):
    try: subprocess.run(cmd, timeout=30, capture_output=True)
    except Exception: pass


sh = os.path.join(OS_DIR, "부서", "00_비서실", "알림.sh")
if os.path.exists(sh):
    run(["bash", sh, "-t", "🎉 설치 완료", f"{CALL}, 고생하셨습니다! 오늘 퍼스널 OS 설치가 공식적으로 완료되었습니다."])
memo = os.path.join(OS_DIR, "elvin_memo.py")
if os.path.exists(memo):
    body = os.path.join(out_dir, "_설치완료_메모.md")
    open(body, "w", encoding="utf-8").write(f"# 🎉 {TODAY} 설치 완료\n\n- 30일 지원: {SUPPORT_END}까지\n- 사용 가이드: {GUIDE}\n- 문의: 브랜디움 카카오 채널 {KAKAO}\n- 내일부터 아침에 \"브리핑\"으로 시작\n")
    run(["python3", memo, "add", "🎉 설치 완료 안내", "--file", body])
log = os.path.join(OS_DIR, "부서", "00_비서실", "업무일지.md")
if os.path.exists(log):
    open(log, "a", encoding="utf-8").write(f"\n- {time.strftime('%Y-%m-%d')} · 00 비서실 · 퍼스널 OS 설치 공식 완료 — 공식 실습 {N_DONE}/{len(STEPS)} 완료(건너뛴 것은 다음에), 30일 지원 {SUPPORT_END}까지\n")
print("설치 완료 화면을 띄웠어요:", out)
