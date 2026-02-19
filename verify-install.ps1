$repoPath = "C:\Users\EX PC\.openclaw\workspace\skills\1ai-skills"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1AI-SKILLS INSTALLATION VERIFICATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check main directory
if (Test-Path $repoPath) {
    Write-Host "[OK] Repository installed at: $repoPath" -ForegroundColor Green
    
    # List skill directories
    Write-Host "`nInstalled Skills:" -ForegroundColor Yellow
    $skillDirs = Get-ChildItem "$repoPath\skills" -Directory -ErrorAction SilentlyContinue
    if ($skillDirs) {
        foreach ($dir in $skillDirs) {
            Write-Host "  - $($dir.Name)" -ForegroundColor Green
        }
    } else {
        Write-Host "  (No skill directories found)" -ForegroundColor Red
    }
    
    # List key files
    Write-Host "`nKey Files:" -ForegroundColor Yellow
    $keyFiles = @('LLM.md', 'README.md', 'INSTALL.md', 'SKILL_INDEX.json', 'package.json')
    foreach ($file in $keyFiles) {
        $path = Join-Path $repoPath $file
        if (Test-Path $path) {
            Write-Host "  [OK] $file" -ForegroundColor Green
        } else {
            Write-Host "  [MISSING] $file" -ForegroundColor Red
        }
    }
    
    # Check node_modules
    if (Test-Path "$repoPath\node_modules") {
        Write-Host "`n[OK] Dependencies installed (node_modules exists)" -ForegroundColor Green
    } else {
        Write-Host "`n[WARNING] node_modules not found - run 'npm install'" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "[FAILED] Repository not found!" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Skills are now available in: $repoPath" -ForegroundColor White
Write-Host "2. Skills auto-activate based on keywords in your requests" -ForegroundColor White
Write-Host "3. Check SKILL_INDEX.json for keyword mappings" -ForegroundColor White
Write-Host "4. See README.md for usage examples" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
