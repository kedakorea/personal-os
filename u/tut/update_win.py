# 퍼스널 OS 업데이트(윈도우) 본체 — update.ps1 이 내려받아 실행한다 (2026-11-11). 한글 경로는 파이썬에서 처리
import os, shutil, subprocess, sys, time, urllib.request
O = os.path.join(os.path.expanduser("~"), "퍼스널OS"); K = os.path.join(O, ".os_키트"); B = "https://mybrandium.com/u/tut/"
if not os.path.isdir(os.path.join(K, "_원본")):
    sys.exit("퍼스널 OS가 깔린 컴퓨터가 아니에요 (퍼스널OS 폴더 없음)")
def get(name, dst):
    data = urllib.request.urlopen(B + name + "?t=%d" % time.time(), timeout=60).read()
    open(dst, "wb").write(data)
get("tutorial.py", os.path.join(K, "공식실습.py"))
get("complete.py", os.path.join(K, "설치완료.py"))
get("phone.py", os.path.join(K, "휴대폰연결안내.py"))
get("serverwatch.py", os.path.join(K, "윈도우_서버지킴이.py"))
pyw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
pyw = pyw if os.path.exists(pyw) else sys.executable
r = subprocess.run(["schtasks", "/Create", "/F", "/TN", "PersonalOS\\serverwatch", "/SC", "MINUTE", "/MO", "5",
                    "/TR", '"%s" -X utf8 "%s"' % (pyw, os.path.join(K, "윈도우_서버지킴이.py"))], capture_output=True, text=True)
print("서버 지킴이 등록:", "완료" if r.returncode == 0 else (r.stderr or r.stdout)[-200:])
tpl = os.path.join(K, "_원본", "CLAUDE.md")
shutil.copy2(tpl, tpl + ".업데이트전_" + time.strftime("%y%m%d%H%M"))
get("claude_tpl.md", tpl)
subprocess.run([sys.executable, "-X", "utf8", os.path.join(K, "적용.py")], capture_output=True)
ok = "공식실습.py" in open(os.path.join(O, "CLAUDE.md"), encoding="utf-8").read()
subprocess.run([sys.executable, "-X", "utf8", os.path.join(K, "휴대폰연결안내.py")])
print("업데이트 완료 — 매니저에게 '공식 실습 시작'이라고 말해 보세요." if ok else "업데이트는 했지만 지침 확인이 안 됐어요. 화면을 찍어 보내 주세요.")
