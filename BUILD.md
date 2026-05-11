# Build Instructions

This project is built with Python and PyInstaller.

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Build the executable

If you run the command from the repository root:

```bash
pyinstaller --onefile --windowed --noconsole --noupx --icon=source/hd2_icon.ico --name "hd2_Allies_of_Humanity_rpc" source/hd2_rpc.py
```

The output file will be created here:

```text
dist/hd2_Allies_of_Humanity_rpc.exe
```

## Notes

This is a PyInstaller executable. Some antivirus engines may flag PyInstaller one-file executables heuristically.

The source code is provided for Nexus Mods moderation and user transparency.
