# ui/main_window.py
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import filedialog, messagebox

from managers.csv_mgr import CsvManager
from ui.sheet_tabs import SheetTabs
from utils.app_state import AppState
from tkinterdnd2 import TkinterDnD, DND_FILES
from managers.hotkeys_mgr import HotkeyManager
from ui.status_bar import StatusBar
from ui.menu_bar import MenuBar
from managers.file_mgr import FileManager
import darkdetect
#from generate_dtch import process_dtch_data  # Import the function
from services.generate_dtch import process_dtch_data


class MainWindow:

    def __init__(self, startup_file=None):
        self.root = TkinterDnD.Tk()
        self.root.title("Excel Manager")
        self.root.geometry("1000x600")

        self.manager = CsvManager()
        self.app_state = AppState

        self.style = ttk.Style(self.root)

        self.status = StatusBar(self.root)
        self.status.pack(fill="x", side="bottom")

        self.tabs = SheetTabs(self.root, self.manager, self.status)
        self.task_panel = None
        self.show_sheet_panel = tk.BooleanVar(value=True)
        self.show_task_panel = tk.BooleanVar(value=False)
        self.autosave = tk.BooleanVar(value=False)

        self.file_manager = FileManager(self, self.manager, self.tabs, self.app_state)

        self.current_theme = tk.StringVar()
        self.current_theme.set("System")

        self._create_menu()
        self._load_last_session()
        self.tabs.select(0)
        self.tabs.pack(fill="both", expand=True)

        self._startup_file = startup_file
        self._startup_load()

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self._on_drop)

        HotkeyManager(self)

    def _create_menu(self):
        menubar = MenuBar(self.root, self)
        self.root.config(menu=menubar)

    def dummy(self):
        pass

    def _show_about_dialog(self):
        messagebox.showinfo(
            "About",
            "Excel Manager.\n© ElMorady 😉",
        )

    def _on_drop(self, event):
        self.file_manager.on_drop(event)

    def _load_last_session(self):
        self.file_manager.load_last_session()

    def new_file(self):
        self.file_manager.new_file()

    def _open_path(self, path):
        self.file_manager._open_path(path)

    def open_file(self):
        self.file_manager.open_file()

    def save_file(self):
        self.file_manager.save_file()

    def save_file_as(self):
        self.file_manager.save_file_as()

    def import_sheet(self):
        self.file_manager.import_sheet()

    def toggle_autosave(self):
        if self.autosave.get():
            self._start_autosave()
        else:
            self._stop_autosave()

    def _start_autosave(self):
        self.autosave_timer = self.root.after(2000, self._autosave)

    def _stop_autosave(self):
        if hasattr(self, 'autosave_timer'):
            self.root.after_cancel(self.autosave_timer)

    def _autosave(self):
        if self.autosave.get():
            self.file_manager.save_file()
            self.autosave_timer = self.root.after(2000, self._autosave)

    def run(self):
        self.root.mainloop()

    def _startup_load(self):
        self.file_manager.startup_load(self._startup_file)

    def toggle_sheet_panel(self):
        if self.show_sheet_panel.get():
            self.tabs.pack(fill="both", expand=True, side=tk.RIGHT)
        else:
            self.tabs.pack_forget()

    def toggle_task_panel(self):
        if self.show_task_panel.get():
            self._show_task_panel()
        else:
            self._hide_task_panel()

    def _show_task_panel(self):
        if self.task_panel is None:
            self.task_panel = ttk.Frame(self.root, width=400)

            self.task_panel_pack_options = {"side": tk.LEFT, "fill": tk.Y}
            self.task_panel.pack(self.task_panel_pack_options)

            self.style.configure("AddButton.TButton", padding=10, font=("Segoe UI", 10))

            add_button = ttk.Button(self.task_panel, text="+", command=self._add_task_line, width=2,
                                     style="AddButton.TButton")
            add_button.pack(pady=5)

            run_button = ttk.Button(self.task_panel, text="Run", command=self._run_tasks, style="AddButton.TButton")
            run_button.pack(pady=5)

            self.task_lines = []
        else:
            self.task_panel.pack(self.task_panel_pack_options)

        self.tabs.pack_forget()
        self.tabs.pack(side=tk.RIGHT, fill="both", expand=True)

    def _hide_task_panel(self):
        if self.task_panel is not None:
            self.task_panel.pack_forget()
        self.tabs.pack_forget()
        self.tabs.pack(fill="both", expand=True)

    def _add_task_line(self):
        task_line = ttk.Frame(self.task_panel)
        task_line.pack(pady=2, padx=5, fill="x")

        options = [
            "Add Row", "Add Column", "Delete Row", "Delete Column",
            "Set Cell Value", "Set Row Values", "Set Column Values", "Clear Region"
        ]
        selected_option = tk.StringVar(value=options[0])
        option_menu = tk.OptionMenu(task_line, selected_option, *options)
        option_menu.config(width=12)
        option_menu.pack(side=tk.LEFT, padx=2)

        textbox1 = ttk.Entry(task_line, width=3)
        textbox1.pack(side=tk.LEFT, padx=2)

        textbox2 = ttk.Entry(task_line, width=3)
        textbox2.pack(side=tk.LEFT, padx=2)

        self.style.configure("DeleteButton.TButton", font=("Segoe UI", 8))

        delete_button = ttk.Button(task_line, text="X", command=lambda: self._delete_task_line(task_line), width=2,
                                    style="DeleteButton.TButton")
        delete_button.pack(side=tk.LEFT, padx=2)

        self.task_lines.append({
            "frame": task_line,
            "option": selected_option,
            "textbox1": textbox1,
            "textbox2": textbox2,
            "delete_button": delete_button
        })

    def _delete_task_line(self, task_line):
        for item in self.task_lines:
            if item["frame"] == task_line:
                item["frame"].destroy()
                self.task_lines.remove(item)
                break

    def _run_tasks(self):
        for item in self.task_lines:
            option = item["option"].get()
            textbox1_value = item["textbox1"].get()
            textbox2_value = item["textbox2"].get()

            print(f"Executing: {option}, {textbox1_value}, {textbox2_value}")
        pass

    def _set_appearance_mode(self, mode):
        self.current_theme.set(mode)
        if mode == "Dark":
            self.root.config(bg="gray12")
        elif mode == "Light":
            self.root.config(bg="SystemButtonFace")
        else:
            if darkdetect.theme() == "Dark":
                self.root.config(bg="gray12")
            else:
                self.root.config(bg="SystemButtonFace")

    def _generate_dtch(self):
        sheet_names = list(self.tabs.views.keys())
        if not sheet_names:
            messagebox.showerror("Error", "No sheets available.")
            return
    
        # Create a new Toplevel window for the sheet selection popup
        popup = tk.Toplevel(self.root)
        popup.title("Select Sheet for DTCH Generation")
    
        # Variable to store the selected sheet name
        selected_sheet = tk.StringVar(value=sheet_names[0])  # Default to the first sheet
    
        # Label for the dropdown
        label = tk.Label(popup, text="Select a sheet:")
        label.pack(pady=5)
    
        # Dropdown menu
        sheet_dropdown = tk.OptionMenu(popup, selected_sheet, *sheet_names)
        sheet_dropdown.pack(pady=5)
    
        # Function to handle the DTCH generation with the selected sheet
        def generate():
            sheet_name = selected_sheet.get()
            if sheet_name:
                data = self.tabs.views[sheet_name].get_data()
                try:
                    output = process_dtch_data(data)
                    output_window = tk.Toplevel(self.root)
                    output_window.title("DTCH Output")
                    text_area = tk.Text(output_window, wrap="none")
                    text_area.pack(expand=True, fill="both")
                    text_area.insert(tk.END, output)
                    text_area.config(state='disabled')
                except Exception as e:
                    messagebox.showerror("Error", f"DTCH Generation Failed: {e}")
                finally:
                    popup.destroy()  # Close the popup after generation
            else:
                messagebox.showerror("Error", "No sheet selected.")
    
        # Select button
        select_button = tk.Button(popup, text="Generate", command=generate)
        select_button.pack(pady=5)

