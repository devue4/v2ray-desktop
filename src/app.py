import v2ray2json
import tkinter as tk
from tkinter import messagebox
import platform
import winreg as reg
import subprocess
import sys
import win32gui
import win32.lib.win32con as win32con
import os

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)

isStart = False

def save_last_config(text):
    with open("last.txt", "w") as file:
        file.write(text)
def load_last_config():
    try:
        with open("last.txt", "r") as file:
            content = file.read()
            text.delete("1.0", tk.END)
            text.insert("1.0", content)
    except FileNotFoundError:
        pass 
def set_proxy_settings(proxy_address, proxy_port):
    try:
        # Check if running on Windows
        if platform.system() != "Windows":
            raise OSError("This script is intended for Windows only.")

        # Define the registry key path for Internet Settings
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

        # Open the registry key
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)

        # Set proxy settings
        reg.SetValueEx(key, "ProxyEnable", 0, reg.REG_DWORD, 1)  # Enable proxy
        reg.SetValueEx(key, "ProxyServer", 0, reg.REG_SZ, f"{proxy_address}:{proxy_port}")

        # Close the registry key
        reg.CloseKey(key)
    except Exception as e:
        messagebox.showerror(f"Error",e)

def disable_proxy_settings():
    try:
        # Check if running on Windows
        if platform.system() != "Windows":
            raise OSError("This script is intended for Windows only.")

        # Define the registry key path for Internet Settings
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"

        # Open the registry key
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)

        # Disable proxy settings
        reg.SetValueEx(key, "ProxyEnable", 0, reg.REG_DWORD, 0)
        # Close the registry key
        reg.CloseKey(key)
    except Exception as e:
        messagebox.showerror(f"Error",e)

def start():
    global isStart
    data = text.get("1.0", tk.END)
    if isStart == False:
        if "vless" in data or "vmess" in data:
            try:
                save_last_config(data)
                set_proxy_settings("127.0.0.1",1080)
                statuslbl.config(text=f"status: start")
                file = open("config.json","+w")
                file.write(v2ray2json.generateConfig(data))
                file.close()
                isStart = True
                with open(os.devnull, 'w') as devnull:
                    subprocess.Popen(["bin/xray.exe"],stdout=devnull)
                messagebox.showinfo("successfully!","VPN started")
            except Exception as e:
                messagebox.showerror(f"Error",e)

        else:
            messagebox.showerror('error',"The configuration is broken")
    else:
        messagebox.showwarning('warning',"VPN is already started")
def stop():
    global isStart
    if isStart == True:
        try:
            subprocess.run(["taskkill", "/F", "/IM", "xray.exe"], check=True)
            disable_proxy_settings()
            statuslbl.config(text=f"status: stop")
            isStart = False
            messagebox.showinfo("successfully!","VPN stopped")
        except Exception as e:
                messagebox.showerror(f"Error",e)
    else:
        messagebox.showerror("Error","VPN not started")
    


def on_closing():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "xray.exe"], check=True)
        disable_proxy_settings()
        root.destroy()
    except Exception as e:
        disable_proxy_settings()
        root.destroy()
root = tk.Tk()
root.iconbitmap("icon.ico")
root.title("v2ray desktop")
root.geometry("270x250")
configlbl = tk.Label(root,text="enter your config:")
configlbl.grid(row=0,column=0)
text = tk.Text(root,width=20,height=10)
text.grid(pady=10,padx=10,row=1,column=0)
statuslbl = tk.Label(root,text=f"status: stop")
statuslbl.grid(row=1,column=1)
startbtn = tk.Button(root, text="start", command=start)
startbtn.grid(row=2,column=0)
stopbtn = tk.Button(root, text="stop", command=stop)
stopbtn.grid(row=2,column=1)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.resizable(width=False, height=False)
load_last_config()
root.mainloop()

