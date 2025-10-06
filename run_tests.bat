@echo off
echo ==========================================
echo     Trello API Automation - Test Runner
echo ==========================================

:: Create virtual environment
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Activate environment
call venv\Scripts\activate

:: Install dependencies
echo Installing required dependencies...
pip install -r requirements.txt

:: Run tests
echo Running Trello API tests...
python main.py > reports\run_log.txt 2>&1

:: Check exit code
if %errorlevel% neq 0 (
    echo Tests failed! Check reports\run_log.txt for details.
) else (
    echo All tests executed successfully!
)

:: Deactivate environment
deactivate
echo Done.
pause
