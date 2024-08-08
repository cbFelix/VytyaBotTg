import atexit
import os
import json
import subprocess

import psutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PID_FILE = os.path.join(BASE_DIR, 'bot_pid.json')
BOT_SCRIPT_PATH = os.path.join(BASE_DIR, 'bot.py')

def save_pid(pid):
    with open(PID_FILE, 'w') as f:
        json.dump({'pid': pid}, f)

def load_pid():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                data = f.read()
                print(f"File content: {data}")
                return json.loads(data).get('pid')
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
    return None


def start_bot():
    pid = load_pid()
    if pid and psutil.pid_exists(pid):
        raise RuntimeError("Bot is already running")
    process = subprocess.Popen(['python', BOT_SCRIPT_PATH])
    save_pid(process.pid)
    return process.pid

def stop_bot():
    pid = load_pid()
    if not pid or not psutil.pid_exists(pid):
        raise RuntimeError("Bot is not running")
    process = psutil.Process(pid)
    process.terminate()
    process.wait()
    os.remove(PID_FILE)


def restart_bot():
    stop_bot()
    start_bot()

def load_state():
    pid = load_pid()
    if pid and psutil.pid_exists(pid):
        return pid
    return None


def cleanup():
    pid = load_pid()
    if pid:
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait()
            os.remove(PID_FILE)
        except Exception as e:
            print(f"Error terminating bot process: {e}")


atexit.register(cleanup)

