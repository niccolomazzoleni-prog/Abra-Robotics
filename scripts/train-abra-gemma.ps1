# Fine-tune Gemma Abra → modello Ollama (locale = online)
param(
    [string]$Dataset = "",
    [int]$Epochs = 3,
    [switch]$InstallOnly,
    [switch]$PromptOnly
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$Venv = Join-Path $Root ".venv-ai"
$Py = Join-Path $Venv "Scripts\python.exe"
$Pip = Join-Path $Venv "Scripts\pip.exe"

if (-not (Test-Path $Venv)) {
    Write-Host "Venv mancante. Esegui prima: .\scripts\setup-abra-ai-local.ps1"
    exit 1
}

$env:Path = "$env:LOCALAPPDATA\Programs\Ollama;$env:Path"

if ($PromptOnly) {
    & $Py (Join-Path $Root "scripts\train_abra_gemma.py") --skip-train
    exit $LASTEXITCODE
}

Write-Host "=== Install / update training deps ===" -ForegroundColor Cyan
& $Pip install --upgrade pip wheel
& $Pip install -r (Join-Path $Root "scripts\requirements-ai.txt")

# pip scrive su stderr durante git clone — non trattarlo come errore fatale
$prevEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& $Pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git" 2>&1 | Out-Host
if ($LASTEXITCODE -ne 0) {
    Write-Host "Unsloth git fallito, provo pypi..." -ForegroundColor Yellow
    & $Pip install unsloth 2>&1 | Out-Host
}
$ErrorActionPreference = $prevEap

if ($InstallOnly) { exit 0 }

$Ds = $Dataset
if (-not $Ds) {
    $Ds = Join-Path $Root "offerte-ai\data\feedback\finetune-dataset.jsonl"
}
if (-not (Test-Path $Ds)) {
    Write-Host "Dataset non trovato: $Ds" -ForegroundColor Red
    Write-Host "1. Usa il Lab → Scarica finetune.jsonl"
    Write-Host "2. Copia in offerte-ai\data\feedback\finetune-dataset.jsonl"
    Write-Host "   oppure: .\scripts\train-abra-gemma.ps1 -Dataset C:\path\finetune-export.jsonl"
    exit 1
}

& $Py (Join-Path $Root "scripts\train_abra_gemma.py") --dataset $Ds --epochs $Epochs
exit $LASTEXITCODE
