# Audit moduli contatti Abra
$root = Split-Path $PSScriptRoot -Parent
$issues = @()
$formFiles = 0
$formCount = 0

Get-ChildItem -Path $root -Recurse -Include *.html -File |
  Where-Object { $_.FullName -notmatch '\\admin\\|\\offerte-ai\\|\\scripts\\|\\.venv' } |
  ForEach-Object {
    $rel = $_.FullName.Substring($root.Length + 1).Replace('\', '/')
    $html = Get-Content $_.FullName -Raw -Encoding UTF8
    $n = ([regex]::Matches($html, 'contact-form|quote-form-top')).Count
    if ($n -eq 0) { return }
    $formFiles++
    $formCount += $n
    if ($html -notmatch 'script\.js') { $issues += "${rel}: missing script.js" }
    if ($html -match 'fetch\(window\.GOOGLE_SCRIPT_URL') { $issues += "${rel}: duplicate inline fetch handler" }
    if ($html -match 'INSERISCI_QUI') { $issues += "${rel}: Apps Script URL placeholder" }
  }

Write-Host "`n=== Audit moduli contatti ==="
Write-Host "File con form: $formFiles"
Write-Host "Istanze form: $formCount"
if ($issues.Count) {
  Write-Host "Problemi:" -ForegroundColor Yellow
  $issues | ForEach-Object { Write-Host "  - $_" }
  exit 1
}
Write-Host "OK - nessun problema" -ForegroundColor Green
