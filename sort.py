import os, sys, json, shutil
import logging

def mkfolders(base_path, names):
    for new_folder_name in names:
        full_path = os.path.join(base_path, new_folder_name)
        try:
            if not os.path.exists(full_path):
                os.mkdir(full_path)
                logging.info(f'Folder "{full_path}" created.')
        except Exception as e:
            logging.error(f'Error creating folder {full_path}: {e}')

def get_safe_path(folder, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_path = os.path.join(folder, filename)
    while os.path.exists(new_path):
        new_filename = f"{name} ({counter}){ext}"
        new_path = os.path.join(folder, new_filename)
        counter += 1
    return new_path

def run_sorting_process(preset_path, folder_to_sort):
    files = os.listdir(folder_to_sort)

    with open(preset_path, "r", encoding="utf-8") as f:
        try: 
            preset = json.load(f)
            mkfolders(folder_to_sort, preset.keys())
        except json.decoder.JSONDecodeError:
            logging.error(f'JSON error in "{preset_path}"')
            return False

    for file in files:
        file_path = os.path.join(folder_to_sort, file)
        if not os.path.isfile(file_path):
            continue

        _, ext = os.path.splitext(file)
        ext = ext.lower()
        target_folder = None

        for folder_name, extensions in preset.items():
            if ext in extensions:
                target_folder = folder_name
                break

        if target_folder is None:
            target_folder = "Extra"
            if target_folder not in preset: preset[target_folder] = []
            if ext not in preset[target_folder]:
                preset[target_folder].append(ext)
            
            with open(preset_path, "w", encoding="utf-8") as f:
                json.dump(preset, f, indent=4, ensure_ascii=False)

        dest_dir = os.path.join(folder_to_sort, target_folder)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        safe_path = get_safe_path(dest_dir, file)
        shutil.move(file_path, safe_path)
        logging.info(f'Moved: {file} -> {target_folder}')
    
    return True