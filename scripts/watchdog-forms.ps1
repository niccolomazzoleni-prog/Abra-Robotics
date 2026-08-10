# Watchdog form + sito Abra Robotics
# Uso: powershell -File scripts/watchdog-forms.ps1
# Task Scheduler: AbraFormsWatchdog ogni 15 min

$ErrorActionPreference = 'Continue'
$Root = Split-Path -Parent $PSScriptRoot
$LogDir = Join-Path $Root 'scripts\watchdog-logs'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir ("forms-{0:yyyy-MM-dd}.log" -f (Get-Date))
$StateFile = Join-Path $LogDir 'last-state.json'
$AlertFile = Join-Path $LogDir 'ALERT-FORMS-DOWN.txt'

$SiteUrl = 'https://abrarobotics.com/'
$ScriptUrl = 'https://abrarobotics.com/script.js'
$Primary = 'https://script.google.com/macros/s/AKfycbw1WeoJYZltyorwQ-8Nftg0DdiOXOV-Zl3MlRegJS2ybhAzaRaqZNpTRamEbHJe2NtK/exec'
$Secondary = 'https://script.google.com/macros/s/AKfycbxPPfh3qZRF0GwnKJicY5rcgdMSRoW_liBenRQValdCPSCM2MrZR_Y6fwrAZOHgCrDW/exec'
$SmokeKey = 'abra2026smoke'
$ExpectedPrimaryToken = 'AKfycbw1WeoJYZltyorwQ-8Nftg0DdiOXOV-Zl3MlRegJS2ybhAzaRaqZNpTRamEbHJe2NtK'

function Write-Log([string]$msg) {
  $line = "{0:yyyy-MM-dd HH:mm:ss}  {1}" -f (Get-Date), $msg
  Add-Content -Path $LogFile -Value $line -Encoding UTF8
  Write-Host $line
}

function Test-Site {
  $o = [ordered]@{ ok = $false; status = 0; ms = 0; error = '' }
  try {
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $r = Invoke-WebRequest -Uri $SiteUrl -UseBasicParsing -TimeoutSec 25
    $sw.Stop()
    $o.status = [int]$r.StatusCode
    $o.ms = [int]$sw.ElapsedMilliseconds
    $o.ok = ($r.StatusCode -eq 200 -and $r.Content -match 'contact-form|abra')
  } catch {
    $o.error = $_.Exception.Message
  }
  return [pscustomobject]$o
}

function Test-LiveScriptConfig {
  $o = [ordered]@{ ok = $false; has_primary = $false; secondary_enabled = $false; error = '' }
  try {
    $r = Invoke-WebRequest -Uri $ScriptUrl -UseBasicParsing -TimeoutSec 25
    $txt = $r.Content
    $o.has_primary = $txt.Contains($ExpectedPrimaryToken)
    # secondary enabled only if URL assigned to a non-empty string literal (not '')
    $o.secondary_enabled = ($txt -match "GOOGLE_SCRIPT_URL_SECONDARY\s*=\s*'https://script\.google\.com")
    $o.ok = $o.has_primary
  } catch {
    $o.error = $_.Exception.Message
  }
  return [pscustomobject]$o
}

function Test-Endpoint([string]$name, [string]$url) {
  $result = [ordered]@{
    name = $name
    url = $url
    get_ok = $false
    get_body = ''
    post_ok = $false
    post_body = ''
    error = ''
  }
  try {
    $g = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 25
    $result.get_body = ($g.Content | Out-String).Trim()
    $result.get_ok = ($g.StatusCode -eq 200 -and $result.get_body -match 'attivo' -and $result.get_body -notmatch 'Sign in|Accedi')
  } catch {
    $result.error = "GET: $($_.Exception.Message)"
  }

  try {
    $load = [int64]((Get-Date).ToUniversalTime().Subtract([datetime]'1970-01-01').TotalMilliseconds - 8000)
    $stamp = Get-Date -Format 'yyyyMMddHHmmss'
    $body = @{
      nome = 'Watchdog'
      email = "watchdog+$stamp@abrarobotics.com"
      telefono = '+393401234567'
      messaggio = 'Watchdog automatico - ignorare'
      origine = 'WATCHDOG'
      pagina = 'watchdog-forms.ps1'
      url = 'https://abrarobotics.com/'
      form_load_time = "$load"
      _smoke_test = $SmokeKey
    }
    $p = Invoke-WebRequest -Uri $url -Method POST -Body $body -ContentType 'application/x-www-form-urlencoded;charset=UTF-8' -UseBasicParsing -TimeoutSec 30
    $result.post_body = ($p.Content | Out-String).Trim()
    if ($result.post_body -match '"ok"\s*:\s*true') {
      $result.post_ok = $true
    } elseif ($result.post_body -match 'autorizzazione|Errore|Sign in|Accedi') {
      $result.post_ok = $false
      $result.error = 'POST rifiutato (permessi foglio o deploy)'
    } else {
      $result.post_ok = $false
      if (-not $result.error) { $result.error = 'POST senza JSON ok' }
    }
  } catch {
    $result.error = "POST: $($_.Exception.Message)"
    $result.post_ok = $false
  }
  return [pscustomobject]$result
}

Write-Log '=== start watchdog forms ==='
$site = Test-Site
$liveJs = Test-LiveScriptConfig
$primary = Test-Endpoint 'primary' $Primary
$secondary = Test-Endpoint 'secondary' $Secondary

Write-Log ("SITE     ok={0} status={1} ms={2}" -f $site.ok, $site.status, $site.ms)
if ($site.error) { Write-Log ("SITE     ERR={0}" -f $site.error) }
Write-Log ("LIVE_JS  ok={0} primary={1} secondary_enabled={2}" -f $liveJs.ok, $liveJs.has_primary, $liveJs.secondary_enabled)
if ($liveJs.error) { Write-Log ("LIVE_JS  ERR={0}" -f $liveJs.error) }
Write-Log ("PRIMARY  GET={0} POST={1} body={2}" -f $primary.get_ok, $primary.post_ok, $primary.get_body)
if ($primary.error) { Write-Log ("PRIMARY  ERR={0}" -f $primary.error) }
$secPreview = if ($secondary.get_body.Length -gt 80) { $secondary.get_body.Substring(0, 80) } else { $secondary.get_body }
Write-Log ("SECONDARY GET={0} POST={1} body={2}" -f $secondary.get_ok, $secondary.post_ok, $secPreview)
if ($secondary.error) { Write-Log ("SECONDARY ERR={0}" -f $secondary.error) }

$criticalOk = ($site.ok -and $liveJs.ok -and $primary.get_ok -and $primary.post_ok)
$state = [ordered]@{
  checked_at = (Get-Date).ToString('o')
  critical_ok = $criticalOk
  site = $site
  live_js = $liveJs
  primary = $primary
  secondary = $secondary
}
$state | ConvertTo-Json -Depth 6 | Set-Content -Path $StateFile -Encoding UTF8

if (-not $criticalOk) {
  Write-Log 'ALERT CRITICAL: sito o form primario NON OK'
  @"
FORM/SITO ABRA DOWN — $(Get-Date -Format o)

Site OK: $($site.ok) ($($site.status))
Live script.js primary URL: $($liveJs.has_primary)
Primary GET: $($primary.get_ok)
Primary POST: $($primary.post_ok)
Error primary: $($primary.error)
Error site: $($site.error)

Azione:
1) Verifica https://abrarobotics.com/
2) Apps Script: Code.gs NON deve essere myFunction vuoto
3) Incolla apps-script/Code.gs e Deploy -> Nuova versione (Chiunque)
4) Controlla foglio Contatti + inbox gio@ / nico@
"@ | Set-Content -Path $AlertFile -Encoding UTF8
  exit 2
}

if (Test-Path $AlertFile) { Remove-Item $AlertFile -Force }

if (-not ($secondary.get_ok -and $secondary.post_ok)) {
  Write-Log 'WARN: secondary non ok (ok se disabilitato in script.js)'
}
if ($liveJs.secondary_enabled -and -not $secondary.post_ok) {
  Write-Log 'WARN: live script.js punta ancora al secondary rotto — serve push di script.js'
}

Write-Log 'OK: sito + primario form sani'
exit 0
