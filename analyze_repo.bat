@echo off
setlocal

REM ============================================================================
REM Repository Analysis Script
REM ============================================================================

cd /d "D:\Projects\automated-business-insight-generator"

echo Generating repository analysis...
echo.

(
echo ==================================================
echo REPOSITORY ANALYSIS
echo ==================================================
echo.

echo === PYTHON FILES ===
dir /s /b *.py 2^>nul ^
| findstr /v /i "\\.venv\\" ^
| findstr /v /i "__pycache__"
echo.

echo === BACKUP FILES ===
dir /s /b *^(*^)*.py 2^>nul
echo.

echo === DUPLICATE FILE CHECK ===
echo.

echo dashboard_metrics.py
dir /s /b dashboard_metrics.py 2^>nul
echo.

echo customer_analysis.py
dir /s /b customer_analysis.py 2^>nul
echo.

echo revenue_insights.py
dir /s /b revenue_insights.py 2^>nul
echo.

echo product_analysis.py
dir /s /b product_analysis.py 2^>nul
echo.

echo executive_summary.py
dir /s /b executive_summary.py 2^>nul
echo.

echo === TOP LEVEL FOLDERS ===
dir /b /ad
echo.

echo === .GITIGNORE ===
if exist ".gitignore" (
    type ".gitignore"
) else (
    echo (No .gitignore found)
)

) > cleanup_analysis.txt

echo.
echo ==========================================
echo Analysis complete.
echo Output saved to:
echo %CD%\cleanup_analysis.txt
echo ==========================================
echo.

pause