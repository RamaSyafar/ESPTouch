import serial
import pyautogui
import time
import ctypes
import os 
import pyperclip
import json # Tambahkan ini untuk membaca config UI

PORT = 'COM16' 
BAUD_RATE = 115200

# --- FUNGSI BACA CONFIG ---
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Jika UI belum pernah dibuka, gunakan settingan asli milikmu
        return {
            "1": "Windows Menu", "2": "Show Workspace", "3": "Show Desktop",
            "4": "AI Combo", "5": "Search Highlighted Text", "10": "Kill Switch"
        }

def print_cheatsheet():
    print("\n" + "="*40)
    print("      🚀 ESP32 TOUCH CONTROLLER 🚀      ")
    print("="*40)
    print(" 1 Tap    : Windows")
    print(" 2 Taps   : Show Workspace")
    print(" 3 Taps   : Show Desktop (Win+D)")
    print(" 4 Taps   : AI Combo (Gemini + Notebook)")
    print(" 5 Taps   : Search Highlighted Text")
    print(" 10 Taps  : KILL SWITCH (Stop Script)")
    print(" 6, 7, 9+ : Panic Lock Screen")
    print(" HOLD     : Shutdown PC (With Confirm)")
    print("="*40)
    print("Waiting for gesture\n")

def open_app(app_name):
    pyautogui.press('win')
    time.sleep(0.1)
    pyautogui.write(app_name, interval=0.1) 
    time.sleep(0.1)
    pyautogui.press('enter')

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
    ser.reset_input_buffer() 
    print_cheatsheet()
except Exception as e:
    print(f"Error: {e}")
    exit()

touch_count = 0
last_touch_time = 0
DOUBLE_TAP_TIMEOUT = 0.5 

print(f"Listening on {PORT}...")

# Load konfigurasi saat script berjalan
config = load_config()

while True:
    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            if data == "TOUCH":
                touch_count += 1
                last_touch_time = time.time()
            elif data == "LONG_PRESS":
                print("Long press detected wait for confirm...")
                pilihan = pyautogui.confirm(
                    text='Really you want to shutdown me?', 
                    title='Confirmation Shutdown', 
                    buttons=['Yes, Shutdown', 'Cancel']
                )

                if pilihan == 'Yes, Shutdown':
                    print("Shutting down... byee...")
                    os.system("shutdown /s /t 30") 
                else:
                    print("Shutdown cancelled.")
                
                ser.reset_input_buffer()
                touch_count = 0

        if touch_count > 0 and (time.time() - last_touch_time) > DOUBLE_TAP_TIMEOUT:
            # Ambil aksi berdasarkan jumlah sentuhan dari config.json
            action = config.get(str(touch_count), "None")

            if action == "Windows Menu":
                pyautogui.hotkey('win')
            elif action == "Show Workspace":
                pyautogui.hotkey('win', 'tab')
            elif action == "Show Desktop":
                pyautogui.hotkey('win', 'd')
            elif action == "AI Combo":
                open_app('google gemini')
                time.sleep(2)
                open_app('notebooklm')
            elif action == "Search Highlighted Text":
                print("Searching highlighted text...")
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.2) 
                query = pyperclip.paste()
                if query.strip():
                    import webbrowser
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                else:
                    print("Clipboard is empty!")
            elif action == "Kill Switch":
                print("Remote Kill Switch Activated!")
                ser.close() 
                exit() 
            elif touch_count > 4:
                # Logika Lock bawaanmu tidak diganggu gugat
                ctypes.windll.user32.LockWorkStation()
            
            touch_count = 0 
            ser.reset_input_buffer() 
            
        time.sleep(0.01) 
            
    except KeyboardInterrupt:
        print("\nProgram stopped.")
        ser.close()
        break