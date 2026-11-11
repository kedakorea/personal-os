#!/usr/bin/env python3
"""휴대폰 연결 화면 — 설치기가 휴대폰 주소를 만들면 저절로 띄운다 (2026-11-11 대표님 지시: 링크를 매번 따로 달라고 하지 않게)
사용: python3 휴대폰연결안내.py [--no-open]
- ~/퍼스널OS/결과물/휴대폰연결.html : 큰 QR + 주소 복사 + 아이폰·갤럭시 순서
- 설정.json 의 "보안주소" 를 쓴다. 없으면 휴대폰연결(.command/_윈도우.bat) 을 먼저 실행하라고 안내한다
"""
import html, json, os, sys, webbrowser

OS_DIR = os.path.expanduser("~/퍼스널OS")
try:
    c = json.load(open(os.path.join(OS_DIR, "설정.json"), encoding="utf-8"))
except Exception:
    c = {}
URL = (c.get("보안주소") or "").strip()
MGR, CALL = c.get("실장") or "매니저", c.get("호칭") or "대표님"
E = html.escape
QR = '<div class="qr" id="qr"></div>' if URL else ""
URLROW = (f"""<div class="url"><b id="u">{E(URL)}</b><button onclick="navigator.clipboard.writeText('{E(URL)}');this.textContent='복사됨 ✓'">주소 복사</button></div>"""
          if URL else """<div class="none">아직 휴대폰 주소가 없어요. 퍼스널OS 폴더의 <b>휴대폰연결</b>을 실행한 뒤 다시 열어 주세요.</div>""")
page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>휴대폰 연결 — 퍼스널 OS</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<script src="https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.js"></script>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Pretendard,-apple-system,'Malgun Gothic',sans-serif;background:#faf9f6;color:#1c1c1e;word-break:keep-all}}
.w{{max-width:900px;margin:0 auto;padding:40px 22px}}.k{{font-weight:800;color:#2f7fe6;letter-spacing:2px}}h1{{font-size:38px;line-height:1.25;margin:8px 0 6px}}p.l{{font-size:18px;color:#555}}
.top{{display:grid;grid-template-columns:300px 1fr;gap:26px;align-items:start;margin-top:24px}}.qr{{background:#fff;border:3px solid #1c1c1e;border-radius:22px;padding:18px}}.qr img{{width:100%;display:block}}
.url{{margin-top:20px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:#fff;border:2px solid #e3e1da;border-radius:16px;padding:14px 16px;font-size:17px}}.url b{{flex:1;word-break:break-all}}
button{{border:0;border-radius:99px;background:#1c1c1e;color:#fff;font:800 15px Pretendard;padding:10px 16px;cursor:pointer}}
.st{{display:grid;gap:12px}}.c{{background:#fff;border:2px solid #e3e1da;border-radius:18px;padding:16px 18px}}.c h2{{font-size:19px;margin-bottom:8px}}.c ol{{padding-left:20px;font-size:16px;line-height:1.7}}
.none{{margin-top:20px;background:#fff3cd;border-radius:16px;padding:18px;font-size:17px}}.f{{margin-top:18px;color:#777;font-size:15px;line-height:1.6}}
@media(max-width:700px){{.top{{grid-template-columns:1fr}}}}</style></head><body><div class="w">
<div class="k">MOBILE</div><h1>휴대폰에서도 {E(MGR)}에게 일 맡기기</h1><p class="l">아래 순서대로 하면 휴대폰 홈 화면에 앱이 생겨요. 밖에서도 말하면 이 컴퓨터가 일합니다.</p>
{URLROW}<div class="top">{QR}<div class="st">
<div class="c"><h2>① Tailscale 앱 깔기</h2><ol><li>앱스토어(아이폰)·플레이스토어(갤럭시)에서 <b>Tailscale</b> 설치</li><li>이 컴퓨터와 <b>같은 계정</b>(구글)으로 로그인 → 연결 켜기</li></ol></div>
<div class="c"><h2>② QR 찍고 홈 화면에 추가</h2><ol><li>휴대폰 카메라로 왼쪽 QR을 찍어 주소 열기 (처음엔 30초쯤 걸릴 수 있어요)</li><li><b>아이폰</b>: 사파리 아래 공유 버튼 → <b>홈 화면에 추가</b></li><li><b>갤럭시</b>: 크롬 ⋮ → <b>홈 화면에 추가</b></li><li>홈 화면 앱을 열고 앱 비밀번호 입력 → 알림 허용</li></ol></div>
<div class="c"><h2>갤럭시만 한 가지 더</h2><ol><li>Tailscale 앱 ⚙ → <b>앱별 분할 터널링</b> → 크롬만 켜기 (삼성페이·은행 앱이 막히지 않게)</li></ol></div>
</div></div>
<p class="f">이 화면은 언제든 {E(MGR)}에게 "휴대폰 연결 화면 보여 줘"라고 하면 다시 열려요.</p></div>
<script>try{{const q=qrcode(0,'M');q.addData({json.dumps(URL)});q.make();document.getElementById('qr').innerHTML=q.createImgTag(8,8);}}catch(e){{}}</script></body></html>"""
out_dir = os.path.join(OS_DIR, "결과물"); os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "휴대폰연결.html")
open(out, "w", encoding="utf-8").write(page)
if "--no-open" not in sys.argv:
    webbrowser.open("file://" + out)
print("휴대폰 연결 화면:", out, "· 주소:", URL or "(아직 없음)")
