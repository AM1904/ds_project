# -*- coding: utf-8 -*-
"""
CampusGrid Web Dashboard Launcher
Starts the local Flask backend and automatically opens the user's browser.
"""
import os
import sys
import webbrowser
import threading
import time
import shutil
import subprocess
PORT = 5050
URL = f"http://localhost:{PORT}"


def open_browser():
    time.sleep(1.2)
    print(f"\n>> Opening browser at: {URL}\n")
    try:
        webbrowser.open(URL)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")


if __name__ == "__main__":
    print("=" * 65)
    print("  CAMPUSGRID // CLASH-FREE TIMETABLE & DSA ENGINE")
    print("=" * 65)
    print(f"  Starting web dashboard at {URL}")
    print("  Press Ctrl+C in this terminal to stop the server.")
    print("=" * 65)
    # The UI is a React app in frontend/. Build it on first run so Flask has something to serve.
    root = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(root, "frontend", "dist", "index.html")):
        npm = shutil.which("npm")
        if not npm:
            sys.exit("  Node.js is required once to build the UI: install Node 20+, then run again.")
        print("  Building the React frontend (first run only)...")
        subprocess.run([npm, "install"], cwd=os.path.join(root, "frontend"), check=True)
        subprocess.run([npm, "run", "build"], cwd=os.path.join(root, "frontend"), check=True)

    threading.Thread(target=open_browser, daemon=True).start()

    from web_server import app
    app.run(host="0.0.0.0", port=PORT, debug=False)
