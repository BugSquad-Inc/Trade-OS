#!/usr/bin/env python3
"""
Trade OS — 1-Click Local Environment Launcher
Starts Docker PostgreSQL (pgvector), FastAPI Backend, and Vite Frontend concurrently.

Usage:
    python start_local.py
    or double-click start_local.bat / run start_local.ps1
"""

import os
import sys
import time
import subprocess
import webbrowser
import signal
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"


def log(msg: str, emoji: str = "⚡"):
    print(f"{emoji}  [Trade OS] {msg}")


def check_docker():
    log("Checking PostgreSQL container (docker compose)...", "🐳")
    try:
        res = subprocess.run(
            ["docker", "compose", "ps", "--format", "json"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            check=False
        )
        if "trade_os_postgres" not in res.stdout:
            log("Starting PostgreSQL via docker compose...", "🚀")
            subprocess.run(["docker", "compose", "up", "-d"], cwd=str(ROOT_DIR), check=True)
            time.sleep(2)
        else:
            log("PostgreSQL container is running.", "✅")
    except Exception as e:
        log(f"Notice: Docker check encountered ({e}). Proceeding if DB is already active...", "⚠️")


def main():
    print("=" * 60)
    print("       🌍 TRADE OS — 1-CLICK LOCAL ENVIRONMENT")
    print("=" * 60)

    check_docker()

    # Determine Python executable
    python_exe = sys.executable

    log("Starting FastAPI Backend (port 8000)...", "🔌")
    backend_cmd = [python_exe, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    
    backend_env = os.environ.copy()
    backend_env["PYTHONPATH"] = str(BACKEND_DIR)

    # Use shell=True on Windows for npm execution
    is_win = sys.platform.startswith("win")

    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=str(BACKEND_DIR),
        env=backend_env
    )

    log("Starting Vite React Frontend (port 5173)...", "🎨")
    npm_cmd = "npm run dev" if is_win else ["npm", "run", "dev"]
    frontend_proc = subprocess.Popen(
        npm_cmd,
        cwd=str(FRONTEND_DIR),
        shell=is_win
    )

    log("Services initialized!", "✨")
    print("-" * 60)
    print("  🖥️  Frontend URL:     http://localhost:5173")
    print("  📖  API Documentation: http://localhost:8000/docs")
    print("  🩺  Health Check:      http://localhost:8000/api/v1/health")
    print("  🐳  PostgreSQL:        localhost:5433 (user: tradeos)")
    print("-" * 60)
    print("Press Ctrl+C at any time to cleanly stop all services.")

    # Try opening browser after 2 seconds
    time.sleep(2)
    try:
        webbrowser.open("http://localhost:5173")
    except Exception:
        pass

    def cleanup(signum=None, frame=None):
        log("Shutting down Trade OS services...", "🛑")
        try:
            frontend_proc.terminate()
            backend_proc.terminate()
            if is_win:
                subprocess.run(f"taskkill /F /T /PID {frontend_proc.pid}", shell=True, capture_output=True)
                subprocess.run(f"taskkill /F /T /PID {backend_proc.pid}", shell=True, capture_output=True)
        except Exception:
            pass
        log("All services stopped. Goodbye!", "👋")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        while True:
            # Check if any process died unexpectedly
            if backend_proc.poll() is not None:
                log("Backend process exited unexpectedly!", "❌")
                break
            if frontend_proc.poll() is not None:
                log("Frontend process exited unexpectedly!", "❌")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
