Write-Host "=========================================="
Write-Host "     Trello API Automation - Test Runner"
Write-Host "=========================================="

# Create virtual environment if not exists
if (!(Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# Activate environment
Write-Host "Activating environment..."
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Ensure reports folder exists
if (!(Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Run tests and log output
Write-Host "Running Trello API tests..."
python main.py *>&1 | Tee-Object -FilePath "reports\run_log.txt"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tests failed! Check reports\run_log.txt for details."
} else {
    Write-Host "✅ All tests executed successfully!"
}

# Deactivate environment
deactivate
Write-Host "Execution complete."
