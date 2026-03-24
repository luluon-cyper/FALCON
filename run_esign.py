import os
import sys
import threading
import time
import subprocess
import urllib.request
import ctypes
import streamlit.web.cli as stcli

APP_PORT = 8501
APP_TITLE = "PQC Hybrid Signature"

def wait_for_server():
    url = f"http://localhost:{APP_PORT}/_stcore/health"
    for _ in range(120):
        try:
            response = urllib.request.urlopen(url, timeout=1)
            if response.getcode() == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False

def check_window_exists(title_substring):
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    window_found = False
    def foreach_window(hwnd, lParam):
        nonlocal window_found
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                if title_substring.lower() in buff.value.lower():
                    window_found = True
                    return False
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return window_found

def watch_window_and_kill():
    appeared = False
    for _ in range(60):
        if check_window_exists(APP_TITLE):
            appeared = True
            break
        time.sleep(1)
        
    if not appeared:
        os._exit(0)
        
    while True:
        time.sleep(2)
        if not check_window_exists(APP_TITLE):
            time.sleep(1)
            if not check_window_exists(APP_TITLE):
                os._exit(0)

def open_browser():
    if wait_for_server():
        url = f"http://localhost:{APP_PORT}"
        
        watcher_thread = threading.Thread(target=watch_window_and_kill)
        watcher_thread.daemon = True
        watcher_thread.start()
        
        try:
            pf86 = os.environ.get('PROGRAMFILES(X86)', r'C:\Program Files (x86)')
            pf = os.environ.get('PROGRAMFILES', r'C:\Program Files')
            
            edge_path = os.path.join(pf86, r"Microsoft\Edge\Application\msedge.exe")
            chrome_path = os.path.join(pf, r"Google\Chrome\Application\chrome.exe")
            chrome_path_x86 = os.path.join(pf86, r"Google\Chrome\Application\chrome.exe")
            
            if os.path.exists(edge_path):
                subprocess.Popen([edge_path, f"--app={url}"])
            elif os.path.exists(chrome_path):
                subprocess.Popen([chrome_path, f"--app={url}"])
            elif os.path.exists(chrome_path_x86):
                subprocess.Popen([chrome_path_x86, f"--app={url}"])
            else:
                import webbrowser
                webbrowser.open(url)
        except Exception:
            pass

def run_streamlit():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    app_path = os.path.join(base_dir, "app.py")
    
    sys.argv = [
        "streamlit", 
        "run", 
        app_path, 
        "--server.headless=true", 
        "--global.developmentMode=false",
        "--server.port", str(APP_PORT)
    ]
    
    sys.exit(stcli.main())

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()

    t = threading.Thread(target=open_browser)
    t.daemon = True
    t.start()

    run_streamlit()