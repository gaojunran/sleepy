# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pygetwindow",
#     "requests",
#     "psutil",
#     "python-dotenv",
#     "pyobjc-framework-quartz",
# ]
# ///


import os
import time
import subprocess
import pygetwindow as gw
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

        # 获取窗口标题，MacOS不用调取title属性
        window_title = active_window

        script = """
tell application "System Events"
set frontApp to name of first application process whose frontmost is true
end tell
return frontApp
"""
        app_name = subprocess.check_output(["osascript", "-e", script]).strip().decode()

        # 返回 "应用名 - 窗口标题"
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
