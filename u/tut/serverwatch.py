# -*- coding: utf-8 -*-
"""퍼스널 OS 서버 지킴이 — 윈도우판 (2026-11-11 안자선 이사님 노트북에서 서버가 꺼져 앱이 안 열린 일 뒤)
작업 스케줄러가 5분마다 부른다. 8765 가 안 열려 있으면 시작 프로그램의 퍼스널OS_서버.vbs 로 다시 켜고 기록을 남긴다."""
import os, socket, subprocess, time
NO_WINDOW = 0x08000000
s = socket.socket(); s.settimeout(3)
try:
    s.connect(("127.0.0.1", 8765)); s.close()
except Exception:
    startup = subprocess.run(["powershell", "-NoProfile", "-Command", "[Environment]::GetFolderPath('Startup')"],
                             capture_output=True, text=True, encoding="utf-8", creationflags=NO_WINDOW).stdout.strip()
    vbs = os.path.join(startup, "퍼스널OS_서버.vbs")
    if os.path.exists(vbs):
        subprocess.Popen(["wscript", vbs], creationflags=NO_WINDOW)
    log = os.path.join(os.path.expanduser("~"), "퍼스널OS", ".os_데이터", "서버지킴이.log")
    try:
        open(log, "a", encoding="utf-8").write(time.strftime("%m-%d %H:%M") + " 서버가 꺼져 있어 다시 켬\n")
    except Exception:
        pass
