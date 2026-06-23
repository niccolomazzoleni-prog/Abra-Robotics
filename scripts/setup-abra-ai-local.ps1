# Setup completo AI locale Abra — Ollama + Gemma + modello custom + venv training
# Uso: .\scripts\setup-abra-ai-local.ps1
# Stesso stack in locale e online (Ollama + proxy.py)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $ScriptDir "..")).Path
Set-Location $Root

$OllamaBin = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
if (-not (Test-Path $OllamaBin)) {
    Write-Host "Ollama non trovato. Installazione via winget..."
    winget install Ollama.Ollama --accept-package-agreements --accept-source-agreements
    $OllamaBin = Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
}
$env:Path = "$(Split-Path $OllamaBin);$env:Path"

Write-Host "`n=== Ollama $(ollama --version) ===" -ForegroundColor Cyan

# Avvia servizio Ollama se non risponde
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 3 | Out-Null
} catch {
    Write-Host "Avvio servizio Ollama..."
    Start-Process $OllamaBin -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 4
}

$BaseModel = "gemma4:e4b"
Write-Host "`n=== Download modello base: $BaseModel (~9 GB) ===" -ForegroundColor Cyan
ollama pull $BaseModel

Write-Host "`n=== Creazione modello Abra (system prompt ufficiale) ===" -ForegroundColor Cyan
$Modelfile = Join-Path $Root "offerte-ai\models\abra-assistente\Modelfile"
if (Test-Path $Modelfile) {
    ollama create abra-assistente -f $Modelfile
    Write-Host "Modello 'abra-assistente' pronto (FROM $BaseModel + prompt commerciale)" -ForegroundColor Green
} else {
    Write-Host "Modelfile non trovato, salto create" -ForegroundColor Yellow
}

Write-Host "`n=== Knowledge index ===" -ForegroundColor Cyan
python (Join-Path $Root "scripts\build_knowledge_index.py")

Write-Host "`n=== Venv training (Unsloth, opzionale) ===" -ForegroundColor Cyan
$Venv = Join-Path $Root ".venv-ai"
$Req = Join-Path $Root "scripts\requirements-ai.txt"
$VenvPy = Join-Path $Venv "Scripts\python.exe"
$VenvPip = Join-Path $Venv "Scripts\pip.exe"
if (-not (Test-Path $VenvPy)) {
    python -m venv $Venv --without-pip
    $GetPip = Join-Path $Root "get-pip.py"
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $GetPip
    & $VenvPy $GetPip
    Remove-Item $GetPip -ErrorAction SilentlyContinue
}
& $VenvPip install --upgrade pip wheel 2>$null
if (Test-Path $Req) {
    Write-Host "Installo dipendenze training (può richiedere diversi minuti)..."
    & "$Venv\Scripts\pip.exe" install -r $Req
}

Write-Host "`n=== VERIFICA ===" -ForegroundColor Green
ollama list
Write-Host ""
Write-Host "Chat Lab:     http://127.0.0.1:8765/offerte-ai/"
Write-Host "Admin AI:     http://127.0.0.1:8765/admin/offerte-ai.html"
Write-Host ""
Write-Host "Config consigliata Admin:" -ForegroundColor Yellow
Write-Host "  Modalita:   Ollama locale"
Write-Host "  Modello:    abra-assistente  (oppure gemma4:e4b)"
Write-Host ""
Write-Host "Training:     .\scripts\train-abra-gemma.ps1 -Dataset finetune-export.jsonl"
Write-Host "Deploy web:   .\scripts\deploy-offerte-ai-local.ps1"
Write-Host ""
