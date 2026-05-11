@echo off
cd /d %TEMP%
setlocal EnableExtensions
set "EXE_NAME=hd2_Allies_of_Humanity_rpc.exe"
set "SCRIPT_DIR=%~dp0"

echo ========================================
echo   HD2 Rich Presence - Setup Utility
echo ========================================
echo.
echo [STEP 1] Checking files...
if not exist "%SCRIPT_DIR%%EXE_NAME%" (
    echo ERROR: %EXE_NAME% not found in the current folder!
    echo.
    echo Please put %EXE_NAME% in the same folder as this installer.
    pause
    exit /b 1
)
echo SUCCESS: File found.
echo.

echo [STEP 2] Selecting installation folder...
echo A window will open. Please choose a folder.
for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null; $f = New-Object System.Windows.Forms.FolderBrowserDialog; $f.Description = 'Select installation folder for HD2 Rich Presence:'; if($f.ShowDialog() -eq 'OK') { $f.SelectedPath }"`) do set "TARGET_DIR=%%I"

if "%TARGET_DIR%"=="" (
    echo CANCELLED. Setup aborted.
    pause
    exit /b 0
)
echo SUCCESS: Folder selected.
echo.

echo [STEP 3] Preparing installation directory...
set "INSTALL_PATH=%TARGET_DIR%\hd2_Allies_of_Humanity_rpc"
if not exist "%INSTALL_PATH%" mkdir "%INSTALL_PATH%"
if %errorlevel% neq 0 (
    echo ERROR: Failed to prepare the installation directory.
    echo Please try another folder.
    pause
    exit /b 1
)
echo SUCCESS: Directory ready.
echo.

echo [STEP 4] Installing program...
copy /Y "%SCRIPT_DIR%%EXE_NAME%" "%INSTALL_PATH%\" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to install the program. Setup aborted.
    echo Please try another folder.
    pause
    exit /b 1
)
echo SUCCESS: Program installed.
echo.

echo [STEP 5] Starting the program...
start "" "%INSTALL_PATH%\%EXE_NAME%"
echo SUCCESS: Program launched in background.
echo.

echo ========================================
echo   SETUP COMPLETE
echo ========================================
echo.
echo IMPORTANT:
echo The program is ALREADY RUNNING in the background.
echo You DO NOT need to start it manually before playing.
echo.
echo It will start with Windows automatically.
echo It does NOTHING while HELLDIVERS 2 is not running.
echo.
echo When HELLDIVERS 2 is running, Discord Rich Presence will turn on automatically.
echo.
echo You can close this window now.
echo.

del /F /Q "%SCRIPT_DIR%%EXE_NAME%" >nul 2>&1
if exist "%SCRIPT_DIR%%EXE_NAME%" (
    echo NOTE: Original file could not be deleted.
    echo Please delete it manually when convenient.
) else (
    echo Cleanup complete. Original file removed.
)
echo.
pause
