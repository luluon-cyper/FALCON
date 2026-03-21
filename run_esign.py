import os
import sys
import threading
import time
import subprocess
import streamlit.web.cli as stcli

def open_browser():
    time.sleep(3)
    url = "http://localhost:8501"
    
    try:
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        if os.path.exists(edge_path):
            subprocess.Popen([edge_path, f"--app={url}"])
        else:
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if os.path.exists(chrome_path):
                subprocess.Popen([chrome_path, f"--app={url}"])
            else:
                import webbrowser
                webbrowser.open(url)
    except Exception as e:
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
        "--global.developmentMode=false"
    ]
    
    sys.exit(stcli.main())

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()

    t = threading.Thread(target=open_browser)
    t.daemon = True
    t.start()

    run_streamlit()