# Deployment veloce — preview admin + sito locale
$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $RepoRoot

Write-Host "=== Admin Abra Robotics (locale) ==="
Write-Host "Dashboard:    http://127.0.0.1:8765/admin/"
Write-Host "Statistiche:  http://127.0.0.1:8765/admin/statistiche.html"
Write-Host "Sito home:    http://127.0.0.1:8765/"
Write-Host ""

Start-Process "http://127.0.0.1:8765/admin/"
python -m http.server 8765
