import customtkinter as ctk
import json
import os

CONFIG_FILE = 'config.json'

# Daftar aksi yang sama persis dengan yang ada di kodenya Ilyas
AVAILABLE_ACTIONS = [
    "None", 
    "Windows Menu", 
    "Show Workspace", 
    "Show Desktop", 
    "AI Combo", 
    "Search Highlighted Text", 
    "Kill Switch"
]

# Konfigurasi bawaan sesuai setup aslimu
DEFAULT_CONFIG = {
    "1": "Windows Menu",
    "2": "Show Workspace",
    "3": "Show Desktop",
    "4": "AI Combo",
    "5": "Search Highlighted Text",
    "10": "Kill Switch"
}

class GestureConfigurator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ESP32 Gesture Config")
        self.geometry("400x500")

        self.load_config()
        self.dropdowns = {}

        ctk.CTkLabel(self, text="⚙️ Pengatur Gesture ESP32", font=("Arial", 20, "bold")).pack(pady=20)

        # Buat dropdown untuk tap 1, 2, 3, 4, 5, dan 10
        taps_to_configure = ["1", "2", "3", "4", "5", "10"]
        
        for tap in taps_to_configure:
            frame = ctk.CTkFrame(self)
            frame.pack(pady=8, padx=20, fill="x")
            
            ctk.CTkLabel(frame, text=f"{tap} Taps :", font=("Arial", 14)).pack(side="left", padx=10)
            
            dropdown = ctk.CTkComboBox(frame, values=AVAILABLE_ACTIONS, width=200)
            dropdown.set(self.config.get(tap, "None"))
            dropdown.pack(side="right", padx=10)
            
            self.dropdowns[tap] = dropdown

        ctk.CTkButton(self, text="Save & Apply", command=self.save_config, fg_color="green", hover_color="darkgreen").pack(pady=30)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = DEFAULT_CONFIG

    def save_config(self):
        for key, dropdown in self.dropdowns.items():
            self.config[key] = dropdown.get()
            
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)
        print("Configuration Saved to config.json!")
        self.destroy()

if __name__ == "__main__":
    app = GestureConfigurator()
    app.mainloop()