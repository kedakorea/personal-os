# 퍼스널 OS 업데이트(윈도우) — 공식 실습·완료 화면·휴대폰 연결 화면 (2026-11-11)
# 사용: PowerShell 에서  irm https://mybrandium.com/u/tut/update.ps1 | iex
$ErrorActionPreference = "Stop"
$O = Join-Path $env:USERPROFILE "퍼스널OS"; $K = Join-Path $O ".os_키트"; $B = "https://mybrandium.com/u/tut"
if (-not (Test-Path (Join-Path $K "_원본"))) { Write-Host "퍼스널 OS가 깔린 컴퓨터가 아니에요"; return }
Invoke-WebRequest "$B/tutorial.py" -OutFile (Join-Path $K "공식실습.py") -UseBasicParsing
Invoke-WebRequest "$B/complete.py" -OutFile (Join-Path $K "설치완료.py") -UseBasicParsing
Invoke-WebRequest "$B/phone.py" -OutFile (Join-Path $K "휴대폰연결안내.py") -UseBasicParsing
Copy-Item (Join-Path $K "_원본\CLAUDE.md") (Join-Path $K ("_원본\CLAUDE.md.업데이트전_" + (Get-Date -Format yyMMddHHmm)))
Invoke-WebRequest "$B/claude_tpl.md" -OutFile (Join-Path $K "_원본\CLAUDE.md") -UseBasicParsing
$py = $null
foreach ($c in @("py","python")) { $p = Get-Command $c -ErrorAction SilentlyContinue; if ($p -and ($p.Source -notmatch "WindowsApps")) { $py = $p.Source; break } }
if (-not $py) { $cand = Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python3*\python.exe" -ErrorAction SilentlyContinue | Select-Object -First 1; if ($cand) { $py = $cand.FullName } }
$env:PYTHONUTF8 = "1"
& $py -X utf8 (Join-Path $K "적용.py") | Out-Null
& $py -X utf8 (Join-Path $K "휴대폰연결안내.py")
Write-Host "✅ 업데이트 완료 — 매니저에게 '공식 실습 시작'이라고 말해 보세요."
