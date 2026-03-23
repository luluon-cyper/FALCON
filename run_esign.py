import os
import sys
import threading
import time
import subprocess
import tempfile
import shutil
import streamlit.web.cli as stcli

APP_PORT = 8501

def open_browser():
    time.sleep(3)
    url = f"http://localhost:{APP_PORT}"
    browser_process = None
    
    temp_profile_dir = os.path.join(tempfile.gettempdir(), "esign_browser_profile")

    try:
        pf86 = os.environ.get('PROGRAMFILES(X86)', r'C:\Program Files (x86)')
        pf = os.environ.get('PROGRAMFILES', r'C:\Program Files')
        
        edge_path = os.path.join(pf86, r"Microsoft\Edge\Application\msedge.exe")
        chrome_path = os.path.join(pf, r"Google\Chrome\Application\chrome.exe")
        chrome_path_x86 = os.path.join(pf86, r"Google\Chrome\Application\chrome.exe")
        
        if os.path.exists(edge_path):
            browser_process = subprocess.Popen([edge_path, f"--app={url}", f"--user-data-dir={temp_profile_dir}"])
        elif os.path.exists(chrome_path):
            browser_process = subprocess.Popen([chrome_path, f"--app={url}", f"--user-data-dir={temp_profile_dir}"])
        elif os.path.exists(chrome_path_x86):
            browser_process = subprocess.Popen([chrome_path_x86, f"--app={url}", f"--user-data-dir={temp_profile_dir}"])
        else:
            import webbrowser
            webbrowser.open(url)
    except Exception:
        pass

    if browser_process:
        browser_process.wait()
        try:
            shutil.rmtree(temp_profile_dir, ignore_errors=True)
        except Exception:
            pass
        os._exit(0)

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