# Helldivers2 Allies of Humanity Rich Presence
This repository contains the source code used for the Nexus Mods release.

## Antivirus / VirusTotal Notice

The release executable is built with **PyInstaller**.

PyInstaller one-file Windows executables can sometimes receive false positive detections from antivirus engines or VirusTotal because they bundle a Python runtime and compressed application code into a single `.exe`.

## Uninstall

To uninstall manually:

1. Close the program from Task Manager if it is currently running.
2. Delete the installed `hd2_Allies_of_Humanity_rpc` folder.
3. Remove the Windows Startup entry named:

```text
hd2_Allies_of_Humanity_rpc
```

Startup entry location:

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

## Notes For Nexus Mods Moderation

This tool does not modify Helldivers 2 files.

It only:

- checks for the `helldivers2.exe` process;
- connects to Discord local RPC;
- displays custom Discord Rich Presence;
- writes a current-user Windows Startup entry so it can run automatically.

No administrator privileges are required.
