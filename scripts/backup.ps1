# backup.ps1
$date = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "backup_$date.zip"

Write-Host "Creating backup: $backupFile" -ForegroundColor Cyan

# Files to backup
$files = @(
    "backend/",
    "frontend/",
    "scanner/",
    "reports/",
    "requirements.txt",
    "README.md"
)

Compress-Archive -Path $files -DestinationPath $backupFile -Force
Write-Host "? Backup created: $backupFile" -ForegroundColor Green
