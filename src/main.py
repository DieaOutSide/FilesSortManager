import flet as ft
import os, sys, logging
from sort import run_sorting_process

#logging
if not os.path.exists('./logs'): 
    os.makedirs('./logs')
logging.basicConfig(
    filename='./logs/sort.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8'
)

def main(page: ft.Page):

    #page arguments
    page.title = "File Sorter v1.2"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.icon = "hard-drive.ico"
    page.window.resizable = False
    page.window.height = 450
    page.window.width = 450
    page.window.center()
    page.window.to_front()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {"preset_path": "", "folder_path": ""}

    lbl_preset = ft.Text("No preset selected", color=ft.Colors.GREY_500, size=12)
    lbl_folder = ft.Text("No folder selected", color=ft.Colors.GREY_500, size=12)

    #msg box
    def show_message(text, type):
        if type == 'warn':
            dlg = ft.AlertDialog(
                title=ft.Text("Something went wrong..", color=ft.Colors.RED_300, size=14),
                content=ft.Text(text, size= 14),
                alignment=ft.alignment.center,
                on_dismiss=lambda e: print("Dialog dismissed!"),
                title_padding=ft.padding.all(25),
            )
            page.open(dlg)
        else: 
            dlg = ft.AlertDialog(
                title=ft.Text("INFO", color=ft.Colors.BLUE_300, size=14),
                content=ft.Text(text, size=14),
                alignment=ft.alignment.center,
                on_dismiss=lambda e: print("Dialog dismissed!"),
                title_padding=ft.padding.all(25),
            )
            page.open(dlg)

    def on_preset_result(e: ft.FilePickerResultEvent):
        if e.files:
            state["preset_path"] = e.files[0].path
            lbl_preset.value = os.path.basename(state["preset_path"])
            lbl_preset.color = ft.Colors.BLUE_200
            page.update()

    def on_folder_result(e: ft.FilePickerResultEvent):
        if e.path:
            state["folder_path"] = e.path
            lbl_folder.value = state["folder_path"]
            lbl_folder.color = ft.Colors.BLUE_200
            page.update()

    #preset, folder requests
    preset_picker = ft.FilePicker(on_result=on_preset_result)
    folder_picker = ft.FilePicker(on_result=on_folder_result)
    page.overlay.extend([preset_picker, folder_picker])

    #start sorting
    def start_sorting(e):
        if not state["preset_path"] or not state["folder_path"]:
            show_message("Select both Preset and Folder!", 'warn')
            return
        
        success = run_sorting_process(state["preset_path"], state["folder_path"])
        if success:
            show_message("Sorting completed successfully!", 'info')
            logging.info("Task completed via GUI")

    #elements on the page (add)
    page.add(
        ft.Column(
            [
                ft.Icon(ft.Icons.FOLDER_COPY_ROUNDED, size=50, color=ft.Colors.BLUE_400),
                ft.Text("File Sorter", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.ElevatedButton("Preset JSON", icon=ft.Icons.SETTINGS, on_click=lambda _: preset_picker.pick_files(allowed_extensions=["json"]), width=220),
                lbl_preset,
                ft.ElevatedButton("Target Folder", icon=ft.Icons.FOLDER_OPEN, on_click=lambda _: folder_picker.get_directory_path(), width=220),
                lbl_folder,
                ft.Container(height=20),
                ft.FilledButton("START", icon=ft.Icons.PLAY_ARROW, bgcolor=ft.Colors.GREEN_700, on_click=start_sorting, width=180, height=45),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(
        target=main, 
        assets_dir="assets",
    )