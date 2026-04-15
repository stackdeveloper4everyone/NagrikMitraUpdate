"""NagrikMitra - One-command startup script.

Launches both FastAPI backend and Streamlit frontend.

Usage:
    python run.py           # Start both servers
    python run.py --api     # Start only FastAPI
    python run.py --ui      # Start only Streamlit
    python run.py --reload  # Enable FastAPI auto-reload
"""

import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def safe_print(text: str) -> None:
    """Print text safely on consoles that do not support full Unicode."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def child_env() -> dict:
    """Environment for child processes with UTF-8-safe I/O."""
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    return env


def check_env() -> None:
    """Check if .env file exists and has API key."""
    env_path = os.path.join(BASE_DIR, ".env")
    if not os.path.exists(env_path):
        example_path = os.path.join(BASE_DIR, ".env.example")
        if os.path.exists(example_path):
            import shutil

            shutil.copy2(example_path, env_path)
            safe_print("[WARN] Created .env from .env.example")
            safe_print("       Please add your SARVAM_API_KEY to .env")
        else:
            safe_print("[WARN] No .env file found. Create one with SARVAM_API_KEY=your_key")


def start_api(use_reload: bool = False) -> subprocess.Popen:
    """Start FastAPI server."""
    safe_print("[API] Starting FastAPI backend on http://localhost:8000")
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
    ]
    if use_reload:
        cmd.append("--reload")

    return subprocess.Popen(cmd, cwd=BASE_DIR, env=child_env())


def start_ui() -> subprocess.Popen:
    """Start Streamlit frontend."""
    safe_print("[UI ] Starting Streamlit frontend on http://localhost:8501")
    streamlit_app = os.path.join(BASE_DIR, "frontend", "streamlit_app.py")
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            streamlit_app,
            "--server.port",
            "8501",
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        cwd=BASE_DIR,
        env=child_env(),
    )


def main() -> None:
    safe_print("=" * 60)
    safe_print("  NagrikMitra - Unified Citizen Interaction Assistant")
    safe_print("  Powered by Sarvam AI Cloud")
    safe_print("=" * 60)
    safe_print("")

    check_env()

    args = sys.argv[1:]
    use_reload = "--reload" in args
    processes = []

    if "--api" in args:
        processes.append(start_api(use_reload=use_reload))
    elif "--ui" in args:
        processes.append(start_ui())
    else:
        api_proc = start_api(use_reload=use_reload)
        processes.append(api_proc)
        time.sleep(2)
        ui_proc = start_ui()
        processes.append(ui_proc)

        safe_print("")
        safe_print("[OK ] Both servers running:")
        safe_print("      API:  http://localhost:8000/docs")
        safe_print("      UI:   http://localhost:8501")
        safe_print("")
        safe_print("Press Ctrl+C to stop both servers")

    try:
        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        safe_print("\n[STOP] Shutting down...")
        for proc in processes:
            proc.terminate()
        for proc in processes:
            proc.wait()
        safe_print("[BYE ] Goodbye!")


if __name__ == "__main__":
    main()
