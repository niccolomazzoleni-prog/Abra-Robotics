# Smoke test Apps Script Abra — form + stats + pageview
# Usage: powershell -File scripts/smoke-apps-script.ps1

$ErrorActionPreference = "Stop"
$Base = "https://script.google.com/macros/s/AKfycbwdJ4taKMGrLP79eQDujrx7vxhbmGI-qhkvlD9k9kLqyUGDOWW-_3_HFMAxqvooPaY1/exec"
$StatsKey = "abra2026stats"
$SmokeKey = "abra2026smoke"
$Passed = 0
$Failed = 0

function Assert($name, $cond, $detail) {
  if ($cond) {
    Write-Host "[PASS] $name" -ForegroundColor Green
    if ($detail) { Write-Host "       $detail" }
    $script:Passed++
  } else {
    Write-Host "[FAIL] $name" -ForegroundColor Red
    if ($detail) { Write-Host "       $detail" }
    $script:Failed++
  }
}

Write-Host "`n=== Abra Apps Script smoke tests ===`n"

# 1. Root endpoint
try {
  $root = Invoke-WebRequest -Uri $Base -UseBasicParsing -TimeoutSec 20
  Assert "GET root" ($root.StatusCode -eq 200 -and $root.Content -match "attivo") $root.Content.Trim()
} catch {
  Assert "GET root" $false $_.Exception.Message
}

# 2. Stats JSON
try {
  $stats = Invoke-WebRequest -Uri "$Base`?action=stats&key=$StatsKey" -UseBasicParsing -TimeoutSec 30
  $json = $stats.Content | ConvertFrom-Json
  Assert "GET stats ok" ($json.ok -eq $true) ("GA4 configured: $($json.ga4.configured)")
  if ($json.links.sheet) { Write-Host "       Sheet: $($json.links.sheet)" }
} catch {
  Assert "GET stats ok" $false $_.Exception.Message
}

# 3. Honeypot — must not crash
try {
  $body = @{
    website = "http://spam.bot"
    nome = "Bot"
    email = "bot@spam.com"
    telefono = "1234567890"
    messaggio = "spam message here"
    form_load_time = [int64]((Get-Date).ToUniversalTime().Subtract([datetime]"1970-01-01").TotalMilliseconds - 5000)
  } | ConvertTo-Json
  $r = Invoke-WebRequest -Uri $Base -Method POST -Body $body -ContentType "application/json" -UseBasicParsing -TimeoutSec 20
  Assert "POST honeypot" ($r.Content -match '"ok"\s*:\s*true') "returns ok, no crash"
} catch {
  Assert "POST honeypot" $false $_.Exception.Message
}

# 4. Pageview beacon
try {
  $pv = @{
    type = "pageview"
    path = "/smoke-test"
    referrer = "https://abrarobotics.com/"
    lang = "it"
    mobile = $false
  } | ConvertTo-Json
  $r = Invoke-WebRequest -Uri $Base -Method POST -Body $pv -ContentType "application/json" -UseBasicParsing -TimeoutSec 20
  Assert "POST pageview" ($r.Content -match '"ok"\s*:\s*true') "analytics beacon"
} catch {
  Assert "POST pageview" $false $_.Exception.Message
}

# 5. Valid lead smoke (mirror write, no email — requires redeployed Code.gs)
try {
  $load = [int64]((Get-Date).ToUniversalTime().Subtract([datetime]"1970-01-01").TotalMilliseconds - 8000)
  $lead = @{
    nome = "Smoke Test HTTP"
    email = "smoke+$(Get-Date -Format 'yyyyMMddHHmmss')@abrarobotics.com"
    telefono = "+393401234567"
    messaggio = "Smoke test HTTP mirror fogli — ignorare"
    origine = "SMOKETEST"
    pagina = "smoke-apps-script.ps1"
    url = "https://abrarobotics.com/"
    form_load_time = $load
    _smoke_test = $SmokeKey
  } | ConvertTo-Json
  $r = Invoke-WebRequest -Uri $Base -Method POST -Body $lead -ContentType "application/json" -UseBasicParsing -TimeoutSec 25
  Assert "POST lead smoke" ($r.Content -match '"ok"\s*:\s*true') "dual-write aggregato + legacy"
} catch {
  Assert "POST lead smoke" $false $_.Exception.Message
}

Write-Host "`n=== Results: $Passed passed, $Failed failed ===`n"
if ($Failed -gt 0) { exit 1 }
