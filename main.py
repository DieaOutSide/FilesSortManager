import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import os
from sort import run_sorting_process

if not os.path.exists('./logs'): os.makedirs('./logs')
logging.basicConfig(
    filename='./logs/sort.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8'
)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter v1.1")
        self.root.geometry("250x220")
        
        self.preset_path = ""
        self.folder_path = ""

        # UI Elements
        tk.Label(root, text="File Sorter Tool",bg="#252525",fg="#DFDFDF", font=("Arial", 12, "bold")).pack(pady=10)

        #Background
        root.configure(bg="#252525")

        # Preset Button
        self.btn_preset = tk.Button(root, text="1. Select Preset JSON", bg="#505050",fg="#D1D1D1", command=self.select_preset, width=25)
        self.btn_preset.pack(pady=5)
        self.lbl_preset = tk.Label(root, text="No file selected", bg="#252525", fg="#D1D1D1", font=("Arial", 8))
        self.lbl_preset.pack()

        # Folder Button
        self.btn_folder = tk.Button(root, text="2. Select Folder",bg="#505050",fg="#D1D1D1", command=self.select_folder, width=25)
        self.btn_folder.pack(pady=5)
        self.lbl_folder = tk.Label(root, text="No folder selected",bg="#252525", fg="#D1D1D1", font=("Arial", 8))
        self.lbl_folder.pack()

        # Start Button
        self.btn_start = tk.Button(root, text="START SORTING", bg="#198546", fg="white", 
                                   font=("Arial", 10, "bold"), command=self.start, width=20)
        self.btn_start.pack(pady=20)

    def select_preset(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.preset_path = path
            self.lbl_preset.config(text=os.path.basename(path), fg="black")

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path = path
            self.lbl_folder.config(text=path, fg="black")

    def start(self):
        if not self.preset_path or not self.folder_path:
            messagebox.showwarning("Error", "Please select both Preset and Folder!")
            return
        
        success = run_sorting_process(self.preset_path, self.folder_path)
        if success:
            messagebox.showinfo("Done", "Sorting completed successfully!")
            logging.info("Task completed via GUI")

if __name__ == "__main__":
    root = tk.Tk()
    try: root.iconbitmap('./assets/hard-drive.ico')
    except: pass
    
    app = App(root)
    root.mainloop()