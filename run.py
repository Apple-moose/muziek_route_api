import subprocess

if __name__ == "__main__":
    subprocess.run([".venv/bin/uvicorn", "main:app", "--host", "127.0.0.1", "--port", "7000", "--reload"])
