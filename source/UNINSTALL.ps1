$ErrorActionPreference = "SilentlyContinue"

$appName = "hd2_Allies_of_Humanity_rpc"
$exeName = "hd2_Allies_of_Humanity_rpc.exe"
$installFolderName = "hd2_Allies_of_Humanity_rpc"
$runKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"

function Write-Blank {
    Write-Host ""
}

function Pause-End {
    Write-Blank
    Write-Host "Press Enter to close this window."
    [void][Console]::ReadLine()
}

function Get-InstalledExePath {
    $process = Get-Process -Name "hd2_Allies_of_Humanity_rpc" -ErrorAction SilentlyContinue |
        Where-Object { $_.Path } |
        Select-Object -First 1

    if ($process -and $process.Path) {
        return $process.Path
    }

    $startupValue = (Get-ItemProperty -Path $runKey -Name $appName -ErrorAction SilentlyContinue).$appName
    if ($startupValue) {
        return $startupValue.Trim().Trim('"')
    }

    return $null
}

Clear-Host
Write-Host "========================================"
Write-Host "  HD2 Rich Presence - Uninstall Utility"
Write-Host "========================================"
Write-Blank
Write-Host "This will remove HD2 Rich Presence from your computer."
Write-Blank

Write-Host "[STEP 1] Finding the installed program..."
$installExe = Get-InstalledExePath

if (-not $installExe) {
    Write-Blank
    Write-Host "ERROR: The installed program could not be found automatically."
    Write-Blank
    Write-Host "If the program folder still exists, please delete it manually."
    Write-Host "You can also delete this uninstaller file manually."
    Pause-End
    exit 1
}

$installExeItem = Get-Item -LiteralPath $installExe -ErrorAction SilentlyContinue
if (-not $installExeItem -or $installExeItem.Name -ine $exeName) {
    Write-Blank
    Write-Host "ERROR: The found file does not look like the HD2 Rich Presence program."
    Write-Host "Found file:"
    Write-Host $installExe
    Write-Blank
    Write-Host "Nothing was deleted."
    Pause-End
    exit 1
}

$installDir = $installExeItem.Directory
if (-not $installDir -or $installDir.Name -ine $installFolderName) {
    Write-Blank
    Write-Host "ERROR: The install folder does not look safe to delete automatically."
    Write-Host "Found folder:"
    Write-Host $(if ($installDir) { $installDir.FullName } else { "Unknown" })
    Write-Blank
    Write-Host "Nothing was deleted."
    Write-Host "Please delete the folder manually if needed."
    Pause-End
    exit 1
}

Write-Host "SUCCESS: Installed program found."
Write-Host "Installation folder:"
Write-Host $installDir.FullName
Write-Blank

Write-Host "[STEP 2] Stopping the background program..."
Get-Process -Name "hd2_Allies_of_Humanity_rpc" -ErrorAction SilentlyContinue |
    Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host "SUCCESS: Program stopped or was not running."
Write-Blank

Write-Host "[STEP 3] Removing Windows Startup entry..."
Remove-ItemProperty -Path $runKey -Name $appName -ErrorAction SilentlyContinue
Write-Host "SUCCESS: Windows Startup entry removed or was not present."
Write-Blank

Write-Host "[STEP 4] Removing installed files..."
Remove-Item -LiteralPath $installDir.FullName -Recurse -Force -ErrorAction SilentlyContinue

if (Test-Path -LiteralPath $installDir.FullName) {
    Write-Blank
    Write-Host "ERROR: The installed folder could not be removed."
    Write-Blank
    Write-Host "Please delete this folder manually:"
    Write-Host $installDir.FullName
    Pause-End
    exit 1
}

Write-Host "SUCCESS: Installed files removed."
Write-Blank
Write-Host "========================================"
Write-Host "  UNINSTALL COMPLETE"
Write-Host "========================================"
Write-Blank
Write-Host "HD2 Rich Presence has been removed."
Write-Blank
Write-Host "You can now delete this uninstaller file manually."
Pause-End
