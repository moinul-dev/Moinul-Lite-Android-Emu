import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

SDK_ROOT = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk")
EMU_EXE = os.path.join(SDK_ROOT, "emulator", "emulator.exe")
ADB_EXE = os.path.join(SDK_ROOT, "platform-tools", "adb.exe")
AVD_NAME = "Moinul_Lite_GMS"


def optimize_ram():
    apps_to_kill = ["msedge.exe", "chrome.exe", "brave.exe", "OneDrive.exe"]
    for app in apps_to_kill:
        subprocess.run(
            ["taskkill", "/F", "/IM", app],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    status_label.config(
        text="Status: RAM Optimized! Heavy background apps closed.", fg="#00ff88"
    )


def launch_emulator():
    optimize_ram()
    if os.path.exists(EMU_EXE):
        subprocess.Popen(
            [
                EMU_EXE,
                "-avd",
                AVD_NAME,
                "-memory",
                "2048",
                "-cores",
                "2",
                "-gpu",
                "swiftshader_indirect",
                "-feature",
                "-Vulkan",
            ]
        )
        status_label.config(text="Status: Booting Google GMS Android...", fg="#00d4ff")
    else:
        status_label.config(
            text="Status: Engine not found! Run setup.ps1 first.", fg="#ffcc00"
        )
        messagebox.showinfo(
            "Setup Info",
            "Run setup.ps1 in PowerShell first to download the Google Android Engine.",
        )


def open_play_store():
    adb = ADB_EXE if os.path.exists(ADB_EXE) else "adb"
    subprocess.run(
        [
            adb,
            "shell",
            "monkey",
            "-p",
            "com.android.vending",
            "-c",
            "android.intent.category.LAUNCHER",
            "1",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    status_label.config(text="Status: Launched Google Play Store!", fg="#00ff88")


def install_apk():
    apk_file = filedialog.askopenfilename(
        title="Select APK File", filetypes=[("Android APK", "*.apk")]
    )
    if apk_file:
        adb = ADB_EXE if os.path.exists(ADB_EXE) else "adb"
        status_label.config(text="Status: Installing APK...", fg="#ffcc00")
        root.update()
        res = subprocess.run(
            [adb, "install", "-r", apk_file], capture_output=True, text=True
        )
        if "Success" in res.stdout:
            status_label.config(
                text="Status: APK Installed Successfully!", fg="#00ff88"
            )
        else:
            messagebox.showerror("Error", res.stderr or res.stdout)


def debloat_emulator():
    adb = ADB_EXE if os.path.exists(ADB_EXE) else "adb"
    subprocess.run(
        [adb, "shell", "settings", "put", "global", "window_animation_scale", "0"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        [adb, "shell", "settings", "put", "global", "transition_animation_scale", "0"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    status_label.config(
        text="Status: Animations Disabled! Maximum Speed Unlocked.", fg="#00ff88"
    )


root = tk.Tk()
root.title("Moinul's Lite Android Emulator (Google GMS Edition)")
root.geometry("460x390")
root.configure(bg="#12161f")
root.resizable(False, False)

tk.Label(
    root,
    text="MOINUL ANDROID EMULATOR",
    font=("Segoe UI", 15, "bold"),
    bg="#12161f",
    fg="#00ff88",
).pack(pady=(20, 5))
tk.Label(
    root,
    text="Lightweight Controller • Official Google Play Services",
    font=("Segoe UI", 9),
    bg="#12161f",
    fg="#8b9bb4",
).pack(pady=(0, 20))

btn_style = {
    "font": ("Segoe UI", 10, "bold"),
    "width": 34,
    "bd": 0,
    "pady": 8,
    "cursor": "hand2",
}

tk.Button(
    root,
    text="1. Optimize RAM & Boot Android",
    bg="#00ff88",
    fg="#0a0e14",
    command=launch_emulator,
    **btn_style,
).pack(pady=6)
tk.Button(
    root,
    text="2. Open Google Play Store",
    bg="#1f2937",
    fg="#ffffff",
    command=open_play_store,
    **btn_style,
).pack(pady=6)
tk.Button(
    root,
    text="3. Install Custom APK from PC",
    bg="#1f2937",
    fg="#ffffff",
    command=install_apk,
    **btn_style,
).pack(pady=6)
tk.Button(
    root,
    text="4. Boost Emulator UI Speed",
    bg="#1f2937",
    fg="#ffcc00",
    command=debloat_emulator,
    **btn_style,
).pack(pady=6)

status_label = tk.Label(
    root, text="Status: Ready", font=("Segoe UI", 9), bg="#12161f", fg="#8b9bb4"
)
status_label.pack(side="bottom", pady=15)

root.mainloop()
