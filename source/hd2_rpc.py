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
PRESENCE_REFRESH_INTERVAL = 30
RPC_BACKOFF_BASE = 10
RPC_BACKOFF_MAX = 30
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
current_game_pid = None
presence_active = False
last_presence_update = 0
next_rpc_attempt = 0
rpc_failure_count = 0

def _get_game_pid():
    try:
        for p in psutil.process_iter(['name', 'pid']):
            if p.info['name'] and p.info['name'].lower() == PROCESS_NAME:
                return p.info['pid']
    except Exception:
        return None
    return None

def _schedule_rpc_retry():
    global next_rpc_attempt, rpc_failure_count
    rpc_failure_count += 1
    delay = min(RPC_BACKOFF_BASE * rpc_failure_count, RPC_BACKOFF_MAX)
    next_rpc_attempt = time.time() + delay

def _reset_rpc_retry():
    global next_rpc_attempt, rpc_failure_count
    next_rpc_attempt = 0
    rpc_failure_count = 0

def _connect_rpc():
    global rpc
    if rpc is not None:
        return True

    if time.time() < next_rpc_attempt:
        return False

    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
        _reset_rpc_retry()
        return True
    except Exception:
        rpc = None
        _schedule_rpc_retry()
        return False

def _disconnect_rpc():
    global rpc, presence_active, last_presence_update
    if rpc:
        active_rpc = rpc
        rpc = None
        try:
            active_rpc.clear()
        except Exception:
            pass
        try:
            active_rpc.close()
        except Exception:
            pass
    presence_active = False
    last_presence_update = 0

def _send_presence_update(pid):
    global rpc, game_start_time, presence_active, last_presence_update
    if not rpc:
        return False

    if not pid:
        _disconnect_rpc()
        return False

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
        last_presence_update = time.time()
        return True
    except Exception:
        _disconnect_rpc()
        _schedule_rpc_retry()
        return False

def main():
    global first_detected, game_start_time, current_game_pid
    setup_autostart()

    while True:
        try:
            now = time.time()
            pid = _get_game_pid()
            if pid:
                if current_game_pid != pid:
                    _disconnect_rpc()
                    _reset_rpc_retry()
                    current_game_pid = pid
                    first_detected = now
                    game_start_time = None
                elif first_detected is None:
                    first_detected = now

                if now - first_detected >= LAUNCH_DELAY:
                    if rpc is None:
                        _connect_rpc()
                    
                    if rpc and (not presence_active or now - last_presence_update >= PRESENCE_REFRESH_INTERVAL):
                        _send_presence_update(pid)
                else:
                    if rpc:
                        _disconnect_rpc()
            else:
                if first_detected is not None or current_game_pid is not None or rpc is not None:
                    _disconnect_rpc()
                    _reset_rpc_retry()
                    first_detected = None
                    game_start_time = None
                    current_game_pid = None

            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(CHECK_INTERVAL)

    _disconnect_rpc()

if __name__ == "__main__":
    main()
