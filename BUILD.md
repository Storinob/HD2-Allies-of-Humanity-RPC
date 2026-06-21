# Build Instructions

This project is built with Python and Nuitka.

## 1. Install dependencies

To compile the project, Nuitka requires a C++ compiler installed on your system. 

* If you don't have one, Nuitka will automatically prompt you and download a free, pre-configured **MinGW-w64** compiler during the first build execution.
```bash
pip install -r requirements.txt
```

## 2. Build the executable

If you run the command from the repository root:

```bash
nuitka --standalone --onefile --windows-disable-console --windows-icon-from-ico=source/hd2_icon.ico --output-filename="hd2_Allies_of_Humanity_rpc" source/hd2_rpc.py
```

The output file will be created inside the current directory:

```text
hd2_Allies_of_Humanity_rpc.exe
```

## Notes

Unlike old PyInstaller builds, compiling with Nuitka translates Python scripts into native C++ code. This prevents the application from being flagged as malware by anti-virus heuristics, ensures faster startup times, and results in a clean, independent binary file.

The source code is provided for Nexus Mods moderation and user transparency.
