# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pygetwindow",
#     "requests",
#     "psutil",
#     "pywin32",
#     "python-dotenv",
# ]
# ///


import os
import time
import pygetwindow as gw
import psutil
import win32process
import requests
import dotenv

# 读取环境变量
dotenv.load_dotenv()


def get_foreground():
    try:
        # 获取当前前台窗口
        active_window = gw.getActiveWindow()
        if not active_window:
            return ""

        # 获取窗口标题
        window_title = active_window.title

        # 获取应用名
        hwnd = active_window._hWnd
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid)
        app_name = process.name()  # 获取应用程序名称

        return f"{app_name} - {window_title}"
    except Exception as e:
        return ""


def main():
    supabase_url = os.getenv("VITE_SUPABASE_URL")
    supabase_key = os.getenv("VITE_SUPABASE_ANON_KEY")

    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Prefer": "return=minimal",
        "Content-Type": "application/json",
    }
    while True:
        app = get_foreground()

        data = {
            "source": "2",  # PC
            "app": app,
        }

        response = requests.post(
            f"{supabase_url}/rest/v1/records", headers=headers, json=data
        )
        print(response, app)

        time.sleep(60)


if __name__ == "__main__":
    main()
