import os
import sys
import time
import winreg
import psutil
from pypresence import Presence

CLIENT_ID = "1500137093844963601"
PROCESS_NAME = "helldivers2.exe"
LAUNCH_DELAY = 20
CHECK_INTERVAL = 5
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "hd2_Allies_of_Humanity_rpc"

def setup_autostart():
    exe_path = os.path.abspath(sys.argv[0])
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ) as key:
            val, _ = winreg.QueryValueEx(key, APP_NAME)
            if os.path.normcase(val.replace('"', '').strip()) == os.path.normcase(exe_path):
                return
    except FileNotFoundError:
        pass
    except Exception:
        pass
    
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
    except Exception:
        pass

rpc = None
game_start_time = None
first_detected = None
presence_active = False

def _get_game_pid():
    for p in psutil.process_iter(['name', 'pid']):
        if p.info['name'] and p.info['name'].lower() == PROCESS_NAME:
            return p.info['pid']
    return None

def _connect_rpc():
    global rpc
    if rpc is not None:
        return True
    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
        return True
    except Exception:
        rpc = None
        return False

def _disconnect_rpc():
    global rpc, presence_active
    if rpc:
        try:
            rpc.clear()
            rpc.close()
        except Exception:
            pass
        rpc = None
    presence_active = False

def _send_initial_update():
    global rpc, game_start_time, presence_active
    if not rpc:
        return

    pid = _get_game_pid()
    if not pid:
        _disconnect_rpc()
        return

    if game_start_time is None:
        try:
            game_start_time = int(psutil.Process(pid).create_time())
        except Exception:
            game_start_time = int(time.time())

    try:
        rpc.update(
            details="Allies of Humanity",
            state="Fighting alongside Super Earth",
            start=game_start_time,
            large_image="icon",
            large_text="Allies of Humanity",
            small_image="small_icon",
            small_text="Helldivers 2",
            buttons=[
                {"label": "Allies of Humanity pg", "url": "https://www.nexusmods.com/helldivers2/mods/10485"},
                {"label": "Current Strategy", "url": "https://hd2galaxy.com"}
            ]
        )
        presence_active = True
    except Exception:
        _disconnect_rpc()

def main():
    global first_detected, game_start_time
    setup_autostart()

    while True:
        try:
            pid = _get_game_pid()
            if pid:
                if first_detected is None:
                    first_detected = time.time()

                if time.time() - first_detected >= LAUNCH_DELAY:
                    if rpc is None:
                        _connect_rpc()
                    
                    if rpc and not presence_active:
                        _send_initial_update()
                else:
                    if rpc:
                        _disconnect_rpc()
            else:
                if first_detected is not None:
                    _disconnect_rpc()
                    first_detected = None
                    game_start_time = None

            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(CHECK_INTERVAL)

    _disconnect_rpc()

if __name__ == "__main__":
    main()
