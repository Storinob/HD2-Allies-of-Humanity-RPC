# Helldivers 2 Allies of Humanity Rich Presence

Source code repository for the **Helldivers 2 Allies of Humanity Rich Presence** utility.

Nexus Mods page:

https://www.nexusmods.com/helldivers2/mods/13476

## Overview

This is a small Windows background utility that replaces the default Discord activity/Rich Presence for **Helldivers 2** with a custom Rich Presence related to **Allies of Humanity**.

The utility does not modify Helldivers 2 files and does not interact with the game installation directory. It only detects whether the game process is running and communicates with Discord through local Discord RPC.

## Behavior

The program:

- runs silently in the background;
- adds itself to Windows Startup for the current user;
- waits for the `helldivers2.exe` process;
- does nothing while Helldivers 2 is not running;
- waits 20 seconds after detecting the game before enabling custom Rich Presence;
- uses the delay so Discord can detect the original game activity first, including streak tracking;
- connects to Discord local RPC;
- displays custom Discord Rich Presence while the game is running;
- clears Discord Rich Presence after the game is closed.

## Installation Behavior

The installer:

1. asks the user to choose an installation folder;
2. installs the executable into a folder named `hd2_Allies_of_Humanity_rpc`;
3. starts the program in the background;
4. removes the temporary executable from the installer folder after installation.

After the first launch, the program writes a current-user Windows Startup entry so it can run automatically with Windows.

Startup entry name:

```text
hd2_Allies_of_Humanity_rpc
```

Startup entry location:

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

No administrator privileges are required.

## Antivirus / VirusTotal Notice

The release executable is built with **PyInstaller**.

PyInstaller one-file Windows executables can sometimes receive false positive detections from antivirus engines or VirusTotal because they bundle a Python runtime and application code into a single `.exe`.

The source code is provided here for transparency, user review, and Nexus Mods moderation.

## Build Instructions

Build instructions are available here:

[BUILD.md](BUILD.md)

## Dependencies

Python dependencies are listed here:

[requirements.txt](requirements.txt)

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

Compiled downloads are distributed through Nexus Mods. This repository is provided as the source code reference for review.
