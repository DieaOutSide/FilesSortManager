import flet as ft
import os, sys, logging, threading, time, shutil, subprocess
from sort import run_sorting_process

# logging configuration
if not os.path.exists('./logs'): 
    os.makedirs('./logs')
logging.basicConfig(
    filename='./logs/sort.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8'
)

# presets directory initialization
PRESETS_DIR = os.path.abspath("./presets")
if not os.path.exists(PRESETS_DIR):
    os.makedirs(PRESETS_DIR)

def main(page: ft.Page):
    # page configuration
    page.title = "File Sorter v1.3"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.icon = "hard-drive.ico"
    page.window.resizable = False
    page.window.height = 630
    page.window.width = 500
    page.window.center()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = {"preset_path": "", "folder_path": "", "is_loading": False}

    # preset management logic
    def on_preset_select(e):
        state["preset_path"] = e.control.value
        lbl_selected_preset.value = f"Selected: {os.path.basename(e.control.value)}"
        page.update()

    presets_list_column = ft.RadioGroup(
        content=ft.Column(scroll=ft.ScrollMode.ADAPTIVE, height=150, spacing=5),
        on_change=on_preset_select
    )

    def refresh_presets(e=None):
        presets_list_column.content.controls.clear()
        if os.path.exists(PRESETS_DIR):
            files = [f for f in os.listdir(PRESETS_DIR) if f.endswith('.json')]
            for file in files:
                full_path = os.path.join(PRESETS_DIR, file)
                presets_list_column.content.controls.append(
                    ft.Radio(value=full_path, label=file)
                )
            if not files:
                presets_list_column.content.controls.append(ft.Text("No presets found", color=ft.Colors.GREY_500))
        page.update()

    def add_preset(e: ft.FilePickerResultEvent):
        if e.files:
            src = e.files[0].path
            dst = os.path.join(PRESETS_DIR, os.path.basename(src))
            shutil.copy(src, dst)
            refresh_presets()
            show_message(f"Added: {os.path.basename(src)}", "info")

    def delete_preset(e):
        if state["preset_path"] and os.path.exists(state["preset_path"]):
            try:
                os.remove(state["preset_path"])
                state["preset_path"] = ""
                lbl_selected_preset.value = "Preset not selected"
                refresh_presets()
                show_message("Deleted successfully", "info")
            except Exception as ex:
                show_message(f"Error: {ex}", "warn")
        else:
            show_message("Select a preset from the list first!", "warn")

    def open_folder_directory(e):
        try:
            # cross-platform folder opening
            if sys.platform == "win32":
                os.startfile(PRESETS_DIR)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", PRESETS_DIR])
            else:
                subprocess.Popen(["xdg-open", PRESETS_DIR])
        except Exception as ex:
            show_message(f"Could not open folder: {ex}", "warn")

    preset_adder_picker = ft.FilePicker(on_result=add_preset)
    folder_picker = ft.FilePicker(on_result=lambda e: on_folder_result(e))
    page.overlay.extend([preset_adder_picker, folder_picker])

    # UI components
    lbl_selected_preset = ft.Text("Preset not selected", color=ft.Colors.BLUE_200, size=12)
    lbl_folder = ft.Text("No folder selected", color=ft.Colors.GREY_500, size=12)

    preset_actions = ft.Column([
        ft.IconButton(ft.Icons.ADD_CIRCLE, on_click=lambda _: preset_adder_picker.pick_files(allowed_extensions=["json"]), tooltip="Add Preset"),
        ft.IconButton(ft.Icons.REFRESH, on_click=refresh_presets, tooltip="Refresh List"),
        ft.IconButton(ft.Icons.FOLDER, on_click=open_folder_directory, tooltip="Open Presets Folder"),
        ft.IconButton(ft.Icons.DELETE, on_click=delete_preset, tooltip="Delete Selected"),
    ], alignment=ft.MainAxisAlignment.START)

    preset_manager_ui = ft.Container(
        content=ft.Row([
            preset_actions,
            ft.VerticalDivider(width=1),
            ft.Container(content=presets_list_column, expand=True, padding=10)
        ]),
        bgcolor="#2a2a2a",
        border_radius=10,
        height=200,
        padding=5,
        border=ft.border.all(1, ft.Colors.GREY_800)
    )

    # message dialog
    def show_message(text, type_msg):
        title = "Warning" if type_msg == 'warn' else "Info"
        dlg = ft.AlertDialog(title=ft.Text(title), content=ft.Text(text))
        page.open(dlg)

    def on_folder_result(e: ft.FilePickerResultEvent):
        if e.path:
            state["folder_path"] = e.path
            lbl_folder.value = f"Folder: {e.path}"
            lbl_folder.color = ft.Colors.BLUE_200
            page.update()

    # loading animation
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
                    b4.width = 20; b1.width = 50; page.update(); time.sleep(0.4)
                    b1.width = 20; b2.width = 50; page.update(); time.sleep(0.4)
                    b2.width = 20; b3.width = 50; page.update(); time.sleep(0.4)
                    b3.width = 20; b4.width = 50; page.update(); time.sleep(0.4)
                except: break
            else: time.sleep(0.1)

    thread = threading.Thread(target=animate_bubbles, daemon=True)
    thread.start()

    # sorting process execution
    def start_sorting(e):
        if not state["preset_path"] or not state["folder_path"]:
            show_message("Select both Preset and Folder!", 'warn')
            return
        state["is_loading"] = True
        main_layout.visible = False
        loading_row.visible = True
        page.update()

        success = run_sorting_process(state["preset_path"], state["folder_path"])
        time.sleep(0.5)
        
        state["is_loading"] = False
        loading_row.visible = False
        main_layout.visible = True
        page.update()
        if success: show_message("Sorting finished!", 'info')

    # main layout assembly
    main_layout = ft.Column([
        ft.Icon(ft.Icons.FOLDER_COPY_ROUNDED, size=40, color=ft.Colors.BLUE_400),
        ft.Text("File Sorter Manager", size=20, weight="bold"),
        ft.Text("1. Choose Preset", size=14, color=ft.Colors.GREY_400),
        preset_manager_ui,
        lbl_selected_preset,
        ft.Divider(height=10, color="transparent"),
        ft.Text("2. Select Target", size=14, color=ft.Colors.GREY_400),
        ft.ElevatedButton("Select Folder", icon=ft.Icons.FOLDER_OPEN, on_click=lambda _: folder_picker.get_directory_path(), width=250),
        lbl_folder,
        ft.Divider(height=20, color="transparent"),
        ft.FilledButton("START SORTING", icon=ft.Icons.PLAY_ARROW, bgcolor=ft.Colors.GREEN_700, width=200, height=45, on_click=start_sorting),
    ], horizontal_alignment="center")

    page.add(main_layout, loading_row)
    refresh_presets()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")