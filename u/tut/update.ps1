# Personal OS update (Windows) - ASCII only. Usage in PowerShell:  irm https://mybrandium.com/u/tut/update.ps1 | iex
$py = $null
foreach ($c in @("py","python")) { $p = Get-Command $c -ErrorAction SilentlyContinue; if ($p -and ($p.Source -notmatch "WindowsApps")) { $py = $p.Source; break } }
if (-not $py) { $cand = Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python3*\python.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1; if ($cand) { $py = $cand.FullName } }
if (-not $py) { Write-Host "Python not found. Run the Personal OS installer again."; return }
$f = Join-Path $env:TEMP "personalos_update.py"
Invoke-WebRequest "https://mybrandium.com/u/tut/update_win.py" -OutFile $f -UseBasicParsing
$env:PYTHONUTF8 = "1"
& $py -X utf8 $f
