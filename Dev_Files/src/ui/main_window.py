import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
#from tkinter import ttk #will be replaced with ctk equivalents
#from tkinter import filedialog, messagebox #use ctk ones
from tkinterdnd2 import TkinterDnD, DND_FILES
from managers.hotkeys_mgr import HotkeyManager
from ui.status_bar import StatusBar
from ui.menu_bar import MenuBar
from ui.sheet_tabs import SheetTabs
from utils.app_state import AppState
from managers.Sheets_mgr import SheetsManager
from managers.file_mgr import FileManager
import darkdetect
from plugins.error_handler.generate_dtch import DtchGenerator

class MainWindow:

    def __init__(self, startup_file=None):
        self.root = ctk.CTk()  # Use ctk.CTk instead of tk.Tk
        self.root.app = self
        self.root.title("Excel Manager")
        self.root.geometry("1000x600")

        self.manager = SheetsManager()
        self.app_state = AppState

        #self.style = ttk.Style(self.root) #No ttk Style Needed

        self.status = StatusBar(self.root)
        self.status.pack(fill="x", side="bottom")

        self.tabs = SheetTabs(self.root, self.manager, self.status)
        self.task_panel = None
        self.show_sheet_panel = ctk.BooleanVar(value=True)
        self.show_task_panel = ctk.BooleanVar(value=False)
        self.autosave = ctk.BooleanVar(value=False)

        self.file_manager = FileManager(self, self.tabs, self.app_state)

        self.current_theme = ctk.StringVar() #tk.StringVar to ctk.StringVar
        self.current_theme.set("System")

        self._create_menu()
        self._load_last_session()
        # self.tabs.select(0)
        self.tabs.pack(fill="both", expand=True)

        self._startup_file = startup_file
        self._startup_load()

        # self.root.drop_target_register(DND_FILES)
        # self.root.dnd_bind("<<Drop>>", self._on_drop)

        HotkeyManager(self)
        
    def dummy(self):
        pass

    def _create_menu(self):
        menubar = MenuBar(self.root, self)
        self.root.config(menu=menubar)

    def _show_about_dialog(self):
        msg = CTkMessagebox(title="About", message="Excel Manager.\n© ElMorady 😉")

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

            self.task_panel = ctk.CTkFrame(self.root, width=400)

            self.task_panel_pack_options = {
                "side": "left",
                "fill": "y"
            }

            self.task_panel.pack(**self.task_panel_pack_options)

            add_button = ctk.CTkButton(
                self.task_panel,
                text="+",
                command=self._add_task_line,
                width=30
            )
            add_button.pack(pady=5)

            run_button = ctk.CTkButton(
                self.task_panel,
                text="Run",
                command=self._run_tasks
            )
            run_button.pack(pady=5)

            self.task_lines = []

        else:
            self.task_panel.pack(**self.task_panel_pack_options)

        # reposition tabs
        self.tabs.pack_forget()
        self.tabs.pack(side="right", fill="both", expand=True)


    def _hide_task_panel(self):

        if self.task_panel is not None:
            self.task_panel.pack_forget()

        self.tabs.pack_forget()
        self.tabs.pack(fill="both", expand=True)


    def _add_task_line(self):
        task_line = ctk.CTkFrame(self.task_panel) #ttk.Frame to ctk.CTkFrame
        task_line.pack(pady=2, padx=5, fill="x")

        options = [
            "Add Row", "Add Column", "Delete Row", "Delete Column",
            "Set Cell Value", "Set Row Values", "Set Column Values", "Clear Region"
        ]
        #selected_option = tk.StringVar(value=options[0]) #tk.StringVar to ctk.CTkStringVar
        #option_menu = tk.OptionMenu(task_line, selected_option, *options) #tk.OptionMenu is replaced with ctk.CTkComboBox
        #option_menu.config(width=12)
        #option_menu.pack(side=tk.LEFT, padx=2)
        selected_option = ctk.StringVar(value=options[0])
        option_menu = ctk.CTkComboBox(task_line, values=options, variable=selected_option, width=100)
        option_menu.pack(side=tk.LEFT, padx=2)


        textbox1 = ctk.CTkEntry(task_line, width=3) #ttk.Entry to ctk.CTkEntry
        textbox1.pack(side=tk.LEFT, padx=2)

        textbox2 = ctk.CTkEntry(task_line, width=3) #ttk.Entry to ctk.CTkEntry
        textbox2.pack(side=tk.LEFT, padx=2)

        #self.style.configure("DeleteButton.TButton", font=("Segoe UI", 8)) #No Style needed

        delete_button = ctk.CTkButton(task_line, text="X", command=lambda: self._delete_task_line(task_line), width=2) #ttk.Button to ctk.CTkButton
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
        ctk.set_appearance_mode(mode.lower()) #sets the theme
        # if mode == "Dark":
        #     self.root.config(bg="gray12")
        # elif mode == "Light":
        #     self.root.config(bg="SystemButtonFace")
        # else:
        #     if darkdetect.theme() == "Dark":
        #         self.root.config(bg="gray12")
        #     else:
        #         self.root.config(bg="SystemButtonFace")


    def _generate_dtch(self):
        sheet_names = list(self.tabs.views.keys())

        # if not sheet_names:
        #     messagebox.showerror("Error", "No sheets available.")
        #     return

        # # For now, use the first sheet:
        # sheet_name = sheet_names[0]
        # data = self.tabs.views[sheet_name].get_data()

        # try:
        #     output = self.dtch_generator.process_dtch_data(data) #call from the new DtchGenerator class
        #     output_window = ctk.CTkToplevel(self.root)
        #     output_window.title("DTCH Output")
        #     text_area = ctk.CTkTextbox(output_window, wrap="none")
        #     text_area.pack(expand=True, fill="both")
        #     text_area.insert(ctk.END, output)
        #     text_area.configure(state='disabled')
        # except Exception as e:
        #     messagebox.showerror("Error", f"DTCH Generation Failed: {e}")
