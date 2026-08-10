# Notifica i nuovi commit su origin/main a gio@ e nico@ via Outlook (PC locale).
# Uso: powershell -File scripts/notify-repo-commits.ps1
# Task: AbraRepoCommitNotify ogni 15 min

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$LogDir = Join-Path $Root 'scripts\watchdog-logs'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$StateFile = Join-Path $LogDir 'last-notified-commit.txt'
$LogFile = Join-Path $LogDir ("commits-{0:yyyy-MM-dd}.log" -f (Get-Date))
$Recipients = @('gio@abrarobotics.com', 'nico@abrarobotics.com')
$RepoUrl = 'https://github.com/niccolomazzoleni-prog/Abra-Robotics'

function Write-Log([string]$msg) {
  $line = "{0:yyyy-MM-dd HH:mm:ss}  {1}" -f (Get-Date), $msg
  Add-Content -Path $LogFile -Value $line -Encoding UTF8
  Write-Host $line
}

Set-Location $Root
git fetch origin --quiet 2>$null
$latest = (git rev-parse origin/main).Trim()
$subjectLine = (git log -1 --format='%s' origin/main).Trim()
$author = (git log -1 --format='%an <%ae>' origin/main).Trim()
$date = (git log -1 --format='%ci' origin/main).Trim()
$bodyPreview = (git log -1 --format='%b' origin/main).Trim()

$previous = ''
if (Test-Path $StateFile) {
  $previous = (Get-Content $StateFile -Raw -ErrorAction SilentlyContinue).Trim()
}

if ($previous -eq $latest) {
  Write-Log "OK no new commits ($($latest.Substring(0,7)))"
  exit 0
}

# First run: record current tip without flooding inbox
if (-not $previous) {
  Set-Content -Path $StateFile -Value $latest -Encoding UTF8
  Write-Log "INIT baseline $($latest.Substring(0,7)) - $subjectLine"
  exit 0
}

$range = git log --format='- %h %an: %s' "$previous..origin/main"
$rangeText = ($range | Out-String).Trim()
if (-not $rangeText) {
  Set-Content -Path $StateFile -Value $latest -Encoding UTF8
  Write-Log "OK tip moved without commits? $($latest.Substring(0,7))"
  exit 0
}

$subject = "[Abra Robotics] Nuovi commit: $subjectLine"
$body = @"
Ciao,

ci sono nuovi commit sulla repo Abra-Robotics (branch main).

Ultimo:
- SHA: $latest
- Autore: $author
- Data: $date
- Messaggio: $subjectLine

$bodyPreview

Commit dal precedente avviso:
$rangeText

Repo: $RepoUrl
Commit: $RepoUrl/commit/$latest

(Notifica automatica dal PC watchdog Abra)
"@

$outlook = $null
$mail = $null
try {
  $outlook = New-Object -ComObject Outlook.Application
  $mail = $outlook.CreateItem(0)
  $mail.To = ($Recipients -join ';')
  $mail.Subject = $subject
  $mail.Body = $body
  $mail.Send()
  Write-Log "SENT mail to $($Recipients -join ', ') for $($latest.Substring(0,7))"
  Set-Content -Path $StateFile -Value $latest -Encoding UTF8
} catch {
  Write-Log "FAIL send: $($_.Exception.Message)"
  exit 1
} finally {
  if ($mail) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($mail) }
  if ($outlook) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($outlook) }
  [GC]::Collect()
}

exit 0
