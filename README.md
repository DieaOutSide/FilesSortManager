# File Sorter (Alpha v1.1) 📂

A simple and efficient Python tool for automatic file organization. This script sorts files into categorized folders based on their extensions using a customizable JSON preset.

---

### 📋 Overview
Managing a cluttered "Downloads" or "Desktop" folder can be a headache. This tool automates the process:
1. **Scans** your chosen directory.
2. **Matches** file extensions against your custom categories.
3. **Moves** files into organized subfolders.
4. **Auto-updates** your preset file if it encounters new, unknown extensions.

### 🛠 Features
* **File selection** Now uses `flet` dialogs to easily pick your target directory and configuration file .
* **Duplicate Protection:** The script prevents overwriting existing files by automatically adding a counter to the filename:
* **Smart Categorization:** If a file extension isn't in your list, it's moved to an **"Extra"** folder, and the script updates your JSON preset for future use.
* **GUI** Moved from `tkinter` to `flet`, just good design.

---

### ⚙️ Example Configuration (`preset.json`)
You can define your own rules. Here is an expanded example including common formats:

```json
{
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".bmp", ".psd"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".rtf"],
    "Music": [".mp3", ".wav", ".flac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".bat", ".jar"],
    "Coding": [".py", ".js", ".html", ".css", ".json", ".cs", ".cpp", ".java"],
    "Extra": []
}
```

---

### 🚀 Usage
1. **Requirements** Ensure you have Python 3.x installed.
2. **Run** Execute the script via terminal or double-click:
    ```bash
    python main.py # works but there is beter way
    ```
    ```bash
    flet run main.py # runs program directly with flet (just 'flet run' also works)
    ```
    ```bash
    flet run --web #This version contains problems related to folder selection, does not work!
    ```
3. **Setup** Select your `preset.json` file (you can set it up however you like).
4. **Done** Check your folder for the newly organized results!

---

### ⚠️ Project Status
**Note**: This is the first alpha release.

* **Compatibility**: Tested only on Windows 10.
* **Future Updates**: Improvements are planned in everything!

---

*Designed to automate routine tasks. This is my first "project" that I'm posting, so it may contain critical errors. Feedback is welcome!*

---
