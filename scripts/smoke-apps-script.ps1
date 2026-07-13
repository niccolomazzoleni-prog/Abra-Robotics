# Smoke test Apps Script Abra — form + stats + pageview
# Usage: powershell -File scripts/smoke-apps-script.ps1

$ErrorActionPreference = "Stop"

function Get-JsonOrError($response) {
  $c = $response.Content
  if ($c -match '^\s*[\{\[]') { return @{ ok = $true; json = ($c | ConvertFrom-Json) } }
  if ($c -match 'autorizzazione') { return @{ ok = $false; detail = 'Permessi foglio Google mancanti per gio@ - redeploy Code.gs + condividi sheet' } }
  if ($c -match '<html') { return @{ ok = $false; detail = 'Risposta HTML errore (redeploy Apps Script?)' } }
  return @{ ok = $false; detail = $c.Substring(0, [Math]::Min(120, $c.Length)) }
}
$Base = "https://script.google.com/macros/s/AKfycbxtbdMWnnFwmsDxZIZaG5xwHyUEQGaeG5jtoe2VHC8/exec"
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
  $parsed = Get-JsonOrError $stats
  if ($parsed.ok) {
    Assert "GET stats ok" ($parsed.json.ok -eq $true) ("GA4 configured: $($parsed.json.ga4.configured)")
    if ($parsed.json.links.sheet) { Write-Host "       Sheet: $($parsed.json.links.sheet)" }
  } else {
    Assert "GET stats ok" $false $parsed.detail
  }
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
  $parsed = Get-JsonOrError $r
  Assert "POST honeypot" ($parsed.ok -and $parsed.json.ok -eq $true) $(if ($parsed.ok) { "returns ok" } else { $parsed.detail })
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
  $parsed = Get-JsonOrError $r
  Assert "POST pageview" ($parsed.ok -and $parsed.json.ok -eq $true) $(if ($parsed.ok) { "analytics beacon" } else { $parsed.detail })
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
    messaggio = "Smoke test HTTP mirror fogli - ignorare"
    origine = "SMOKETEST"
    pagina = "smoke-apps-script.ps1"
    url = "https://abrarobotics.com/"
    form_load_time = $load
    _smoke_test = $SmokeKey
  } | ConvertTo-Json
  $r = Invoke-WebRequest -Uri $Base -Method POST -Body $lead -ContentType "application/json" -UseBasicParsing -TimeoutSec 25
  $parsed = Get-JsonOrError $r
  Assert "POST lead smoke" ($parsed.ok -and $parsed.json.ok -eq $true) $(if ($parsed.ok) { "dual-write aggregato + legacy" } else { $parsed.detail })
} catch {
  Assert "POST lead smoke" $false $_.Exception.Message
}

Write-Host "`n=== Results: $Passed passed, $Failed failed ===`n"
if ($Failed -gt 0) { exit 1 }
