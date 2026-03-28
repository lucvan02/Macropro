import time
import json
import threading
import pyautogui
import os
from pynput import mouse, keyboard
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# ======================
# CONFIG
# ======================
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.001
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================
# GLOBAL
# ======================
events = []
recording = False
is_playing = False
last_time = None
last_pos = (0, 0)

# ======================
# UTIL & UI HELPERS
# ======================
def get_delay():
    global last_time
    now = time.time()
    delay = now - last_time if last_time else 0
    last_time = now
    return max(delay, 0.001)

def update_status(text, color="black"):
    root.after(0, lambda: status_label.config(text=text, fg=color))

def format_key(key):
    """Chuẩn hóa phím từ pynput sang pyautogui"""
    try:
        return key.char
    except AttributeError:
        k = str(key).replace("Key.", "")
        # Xử lý các phím bổ trợ (Ctrl, Alt, Shift) bị phân biệt trái/phải
        mapping = {
            "ctrl_l": "ctrl", "ctrl_r": "ctrl",
            "alt_l": "alt", "alt_r": "alt", "alt_gr": "alt",
            "shift_l": "shift", "shift_r": "shift",
            "space": "space", "enter": "enter", "backspace": "backspace",
            "tab": "tab", "esc": "esc", "caps_lock": "capslock"
        }
        return mapping.get(k, k)

# ======================
# RECORD LOGIC
# ======================
def on_move(x, y):
    global last_pos
    if recording:
        if abs(x - last_pos[0]) > 8 or abs(y - last_pos[1]) > 8:
            events.append({"type": "move", "x": x, "y": y, "time": get_delay()})
            last_pos = (x, y)

def on_click(x, y, button, pressed):
    if recording:
        # Lấy tên nút chuột (left, right, middle)
        btn_name = str(button).replace("Button.", "")
        events.append({
            "type": "click", 
            "x": x, "y": y, 
            "button": btn_name, 
            "pressed": pressed, 
            "time": get_delay()
        })

def on_scroll(x, y, dx, dy):
    if recording:
        events.append({"type": "scroll", "dy": dy, "time": get_delay()})

def on_press(key):
    global recording
    # Lọc không ghi các phím điều khiển macro
    if key in [keyboard.Key.f6, keyboard.Key.f7, keyboard.Key.f8, keyboard.Key.f9]:
        if key == keyboard.Key.f6: root.after(0, start_record)
        if key == keyboard.Key.f7: root.after(0, stop_record)
        if key == keyboard.Key.f8: root.after(0, lambda: threading.Thread(target=play_macro, daemon=True).start())
        if key == keyboard.Key.f9: root.after(0, stop_all)
        return

    if recording:
        k = format_key(key)
        if k:
            events.append({"type": "key_down", "key": k, "time": get_delay()})

def on_release(key):
    if recording:
        if key in [keyboard.Key.f6, keyboard.Key.f7, keyboard.Key.f8, keyboard.Key.f9]:
            return
        k = format_key(key)
        if k:
            events.append({"type": "key_up", "key": k, "time": get_delay()})

# ======================
# CONTROL & PLAYER
# ======================
def start_record():
    global recording, events, last_time, is_playing
    if recording: return
    is_playing = False
    events = []
    recording = True
    last_time = time.time()
    update_status("🔴 Đang ghi (Lưu cả Chuột Phải/Tổ hợp)...", "red")

def stop_record():
    global recording
    if not recording: return
    recording = False
    filename = simpledialog.askstring("Save", "Tên file:", parent=root)
    if not filename: filename = "macro_" + time.strftime("%H%M%S")
    file_path = os.path.join(BASE_DIR, f"{filename}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)
    update_status(f"✅ Đã lưu: {filename}.json", "green")

def stop_all():
    global recording, is_playing
    recording = False
    is_playing = False
    update_status("⏹ Đã dừng", "black")

def play_macro():
    global is_playing
    if is_playing: return
    try:
        loop_total = int(loop_entry.get())
    except:
        loop_total = 1

    file = filedialog.askopenfilename(initialdir=BASE_DIR, filetypes=[("JSON", "*.json")])
    if not file: return

    with open(file, "r") as f:
        data = json.load(f)

    is_playing = True
    time.sleep(1)

    for i in range(loop_total):
        if not is_playing: break
        update_status(f"▶️ Vòng: {i+1}/{loop_total}", "blue")
        for e in data:
            if not is_playing: break
            time.sleep(max(e["time"], 0.001))
            try:
                if e["type"] == "move":
                    pyautogui.moveTo(e["x"], e["y"])
                elif e["type"] == "click":
                    if e["pressed"]:
                        pyautogui.mouseDown(e["x"], e["y"], button=e.get("button", "left"))
                    else:
                        pyautogui.mouseUp(e["x"], e["y"], button=e.get("button", "left"))
                elif e["type"] == "scroll":
                    pyautogui.scroll(e["dy"])
                elif e["type"] == "key_down":
                    pyautogui.keyDown(e["key"])
                elif e["type"] == "key_up":
                    pyautogui.keyUp(e["key"])
            except: continue

    is_playing = False
    update_status("✅ Hoàn thành", "green")

# ======================
# UI SETUP
# ======================
root = tk.Tk()
root.title("Macro Tool Pro Max")
root.geometry("400x350")
root.attributes("-topmost", True)

tk.Label(root, text="MACRO TOOL PRO MAX", font=("Arial", 14, "bold")).pack(pady=10)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Ghi (F6)", width=15, bg="#e74c3c", fg="white", command=start_record).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Lưu (F7)", width=15, command=stop_record).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Chạy (F8)", width=15, bg="#2ecc71", fg="white", command=lambda: threading.Thread(target=play_macro, daemon=True).start()).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="DỪNG (F9)", width=15, bg="#34495e", fg="white", command=stop_all).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Số lần lặp:").pack()
loop_entry = tk.Entry(root, justify='center')
loop_entry.insert(0, "1")
loop_entry.pack(pady=5)

status_label = tk.Label(root, text="Sẵn sàng", font=("Arial", 10, "italic"))
status_label.pack(pady=10)

# Khởi chạy Listener
mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll).start()
keyboard.Listener(on_press=on_press, on_release=on_release).start()

root.mainloop()
