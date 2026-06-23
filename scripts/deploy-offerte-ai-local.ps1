# Deployment veloce — preview locale (+ check Ollama)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $ScriptDir "..")).Path
Set-Location $Root

$env:Path = "$env:LOCALAPPDATA\Programs\Ollama;$env:Path"
Write-Host "Rigenero knowledge index..."
python (Join-Path $Root "scripts\build_knowledge_index.py")

Write-Host ""
Write-Host "=== Ollama ===" -ForegroundColor Cyan
try {
    $tags = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 3
    $models = ($tags.models | ForEach-Object { $_.name }) -join ", "
    if ($models) { Write-Host "Modelli: $models" -ForegroundColor Green }
    else { Write-Host "Ollama attivo ma nessun modello — esegui: .\scripts\setup-abra-ai-local.ps1" -ForegroundColor Yellow }
} catch {
    Write-Host "Ollama non raggiungibile — esegui: .\scripts\setup-abra-ai-local.ps1" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== APRI NEL BROWSER ==="
Write-Host "Lab Training:      http://127.0.0.1:8765/offerte-ai/"
Write-Host "Widget demo:       http://127.0.0.1:8765/offerte-ai/demo.html"
Write-Host "Crea offerta:      http://127.0.0.1:8765/offerte-ai/offerta.html"
Write-Host "Admin + feedback:  http://127.0.0.1:8765/admin/offerte-ai.html"
Write-Host ""
Write-Host "Locale: auto-config Ollama da offerte-ai/data/local-ai-config.json"
Write-Host ""
Start-Process "http://127.0.0.1:8765/offerte-ai/"
python -m http.server 8765
