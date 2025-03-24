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
import platform
import subprocess
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
            return "没有找到前台窗口"

        # 获取窗口标题
        window_title = active_window.title

        # 获取应用名
        if platform.system() == "Windows":
            # 获取窗口句柄
            hwnd = active_window._hWnd

            # 获取窗口进程 ID
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]

            # 使用 psutil 获取进程名称
            process = psutil.Process(pid)
            app_name = process.name()  # 获取应用程序名称
        elif platform.system() == "Darwin":
            # 使用 AppleScript 获取 macOS 上前台应用的名称
            script = 'tell application "System Events" to get the name of the frontmost application'
            app_name = (
                subprocess.check_output(["osascript", "-e", script]).strip().decode()
            )
        else:
            app_name = "未知应用"

        # 返回 "应用名 - 窗口标题"
        return f"{app_name} - {window_title}"

    except Exception as e:
        return ""


def main():
    # 从环境变量获取 Supabase 的 URL 和密钥
    supabase_url = os.getenv("VITE_SUPABASE_URL")
    supabase_key = os.getenv("VITE_SUPABASE_ANON_KEY")

    # 构建请求头
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
            "app": app,  # 替换成实际变量，如 foreground_app_name
        }

        response = requests.post(
            f"{supabase_url}/rest/v1/records", headers=headers, json=data
        )
        print(response, app)

        time.sleep(60)


if __name__ == "__main__":
    main()
