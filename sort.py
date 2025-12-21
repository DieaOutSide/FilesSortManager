import tkinter as tk
import os, sys, json, shutil
from tkinter import filedialog

def folderinit():
    root = tk.Tk()
    root.withdraw()
    root.iconbitmap('./folder.ico')
    folder_path = filedialog.askdirectory(title="Select directory folder")

    return (folder_path)
def presetinit():
    root = tk.Tk()
    root.withdraw()
    root.iconbitmap('./file.ico')
    preset_path = filedialog.askopenfilename(
        title="Select preset JSON file",
        filetypes=[("JSON files", "*.json")]
    )

    return preset_path
def mkfolders(base_path, names):
    for new_folder_name in names:
        full_path = os.path.join(base_path, new_folder_name)

        try:
            os.mkdir(full_path)
            sys.stdout.write(f"Folder '{full_path}' created. \n")
        except FileExistsError:
            sys.stdout.write(f"Folder '{full_path}' already exist. \n")
        except FileNotFoundError:
            sys.stdout.write(f"Path '{base_path}' not found. \n")
            return KeyError(FileNotFoundError)
        
def get_safe_path(folder, filename):
    name, ext = os.path.splitext(filename)
    counter = 1

    new_path = os.path.join(folder, filename)

    while os.path.exists(new_path):
        new_filename = f"{name} ({counter}){ext}"
        new_path = os.path.join(folder, new_filename)
        counter += 1

    return new_path      
def sort(preset_path):
    path = folderinit()
    files = os.listdir(path)

    with open(preset_path, "r", encoding="utf-8") as f:
        try: 
            preset = json.load(f)
            mkfolders(path, preset.keys())
        except json.decoder.JSONDecodeError:
            sys.stdout.write('Something went wrong. Check preset.json file! \n')

    for file in files:
        _, ext = os.path.splitext(file)
        ext = ext.lower()
        targetf = None

        for foldt, extn in preset.items():
            if ext in extn:
                targetf = foldt
                file_path = os.path.join(path, file)
                folder_path = os.path.join(path, targetf)

                if not os.path.isfile(file_path):
                    continue

                safe_target_path = get_safe_path(folder_path, file)
                shutil.move(file_path, safe_target_path)
                break

        if targetf is None:
            if "Extra" not in preset:
                preset["Extra"] = []

            if ext not in preset["Extra"]:
                preset["Extra"].append(ext)

            temp = os.path.join(path, "Extra")
            if not os.path.exists(temp):
                os.makedirs(temp)

            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):                     
                safe_target_path = get_safe_path(temp, file) 
                shutil.move(file_path, safe_target_path) 

            with open(preset_path, "w", encoding="utf-8") as f:
                json.dump(preset, f, indent=4, ensure_ascii=False)
  
    sys.stdout.write('Task completed')
        
        

sort(presetinit())