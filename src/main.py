import flet as ft
import os, sys, logging
import threading
import time
from sort import run_sorting_process

# logging
if not os.path.exists('./logs'): 
    os.makedirs('./logs')
logging.basicConfig(
    filename='./logs/sort.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8'
)

def main(page: ft.Page):
    # page arguments
    page.title = "File Sorter v1.2"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.icon = "hard-drive.ico"
    page.window.resizable = False
    page.window.height = 450 # Вернул размер назад
    page.window.width = 450
    page.window.center()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {"preset_path": "", "folder_path": "", "is_loading": False}

    #animation
    def create_bubble():
        return ft.Container(
            animate=ft.Animation(600, "bounceOut"),
            width=20,
            height=20,
            border_radius=100,
            bgcolor=ft.Colors.WHITE,
        )

    b1, b2, b3, b4 = create_bubble(), create_bubble(), create_bubble(), create_bubble()
    
    loading_row = ft.Row(
        alignment="center", 
        controls=[b1, b2, b3, b4],
        visible=False
    )

    def animate_bubbles():
        while True:
            if state["is_loading"]:
                try:
                    b4.width = 20; b1.width = 50; page.update()
                    time.sleep(0.4)
                    b1.width = 20; b2.width = 50; page.update()
                    time.sleep(0.4)
                    b2.width = 20; b3.width = 50; page.update()
                    time.sleep(0.4)
                    b3.width = 20; b4.width = 50; page.update()
                    time.sleep(0.4)
                except Exception: break
            else:
                time.sleep(0.1) 

    thread = threading.Thread(target=animate_bubbles, daemon=True)
    thread.start()

    lbl_preset = ft.Text("No preset selected", color=ft.Colors.GREY_500, size=12)
    lbl_folder = ft.Text("No folder selected", color=ft.Colors.GREY_500, size=12)
    
    main_content = ft.Column(
        [
            ft.Icon(ft.Icons.FOLDER_COPY_ROUNDED, size=50, color=ft.Colors.BLUE_400),
            ft.Text("File Sorter", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            ft.ElevatedButton("Preset JSON", icon=ft.Icons.SETTINGS, 
                             on_click=lambda _: preset_picker.pick_files(allowed_extensions=["json"]), width=220),
            lbl_preset,
            ft.ElevatedButton("Target Folder", icon=ft.Icons.FOLDER_OPEN, 
                             on_click=lambda _: folder_picker.get_directory_path(), width=220),
            lbl_folder,
            ft.Container(height=20),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    #/animation
    
    def show_message(text, type_msg):
        title = "Something went wrong.." if type_msg == 'warn' else "INFO"
        color = ft.Colors.RED_300 if type_msg == 'warn' else ft.Colors.BLUE_300
        dlg = ft.AlertDialog(
            title=ft.Text(title, color=color, size=14),
            content=ft.Text(text, size=14),
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

    preset_picker = ft.FilePicker(on_result=on_preset_result)
    folder_picker = ft.FilePicker(on_result=on_folder_result)
    page.overlay.extend([preset_picker, folder_picker])

    btn_start = ft.FilledButton("START", icon=ft.Icons.PLAY_ARROW, bgcolor=ft.Colors.GREEN_700, 
                               width=180, height=45, on_click=lambda e: start_sorting(e))

    def start_sorting(e):
        if not state["preset_path"] or not state["folder_path"]:
            show_message("Select both Preset and Folder!", 'warn')
            return
        
        state["is_loading"] = True
        main_content.visible = False 
        btn_start.visible = False    
        loading_row.visible = True   
        page.update()

        time.sleep(0.5)

        success = run_sorting_process(state["preset_path"], state["folder_path"])
        
        state["is_loading"] = False
        loading_row.visible = False
        main_content.visible = True
        btn_start.visible = True
        page.update()

        if success:
            show_message("Sorting completed successfully!", 'info')

    page.add(
        main_content,
        btn_start,
        ft.Container(height=20),
        loading_row
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")