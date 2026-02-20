@echo off
REM Create Desktop Shortcut for Vibe Coder GUI (Windows)

echo ========================================
echo   Creating Desktop Shortcut...
echo ========================================
echo.

REM Get current directory
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Get desktop path
set DESKTOP=%USERPROFILE%\Desktop

REM Create shortcut using PowerShell
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Vibe Coder.lnk'); $Shortcut.TargetPath = '%SCRIPT_DIR%\run-gui.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.IconLocation = '%SYSTEMROOT%\System32\shell32.dll,13'; $Shortcut.Description = 'Vibe Coder - Autonomous App Factory'; $Shortcut.Save()"

if %errorlevel% equ 0 (
    echo ✅ Desktop shortcut created!
    echo.
    echo   Location: %DESKTOP%\Vibe Coder.lnk
    echo.
    echo   You can now double-click the shortcut to start Vibe Coder!
) else (
    echo ❌ Failed to create shortcut
    echo.
    echo   You can manually create a shortcut to:
    echo   %SCRIPT_DIR%\run-gui.bat
)

echo.
pause
