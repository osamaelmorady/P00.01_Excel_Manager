# ui/menu_bar.py
import tkinter as tk
from tkinter import filedialog, messagebox
from services.polyspace_justifier import PolyspaceApp  # Import PolyspaceApp


class MenuBar(tk.Menu):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
        self._create_tools_menu()
        self._create_help_menu()

    def _create_file_menu(self):
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="New ...", command=self.controller.file_manager.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open ...", command=self.controller.file_manager.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save ...", command=self.controller.file_manager.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.controller.file_manager.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator() 
        file_menu.add_command(label="Insert sheet", command=self.controller.file_manager.import_sheet, accelerator="Ctrl+T")
        file_menu.add_separator()
        file_menu.add_checkbutton(
            label="Autosave",
            variable=self.controller.autosave,
            command=self.controller.toggle_autosave,
            onvalue=True,
            offvalue=False
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.controller.root.quit, accelerator="   Esc")
        self.add_cascade(label="File", menu=file_menu)

    def _create_edit_menu(self):
        edit_menu = tk.Menu(self, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.controller.dummy, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.controller.dummy, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Refresh", command=self._Not_implemented_yet, accelerator="      F5")
        edit_menu.add_command(label="Clear All", command=self.controller.dummy, accelerator=" ")
        edit_menu.add_command(label="Select All", command=lambda: self.controller.tabs.get_active_view().sheet.select_all(), accelerator="Ctrl+A")
        self.add_cascade(label="Edit", menu=edit_menu)

    def _create_view_menu(self):
        view_menu = tk.Menu(self, tearoff=0)

        window_menu = tk.Menu(view_menu, tearoff=0)
        window_menu.add_command(label="Full Screen", accelerator="F11", command=self._Not_implemented_yet)
        window_menu.add_command(label="Window", accelerator="F12", command=self._Not_implemented_yet)
        view_menu.add_cascade(label="Window", menu=window_menu)

        appearance_menu = tk.Menu(view_menu, tearoff=0)
        appearance_menu.add_radiobutton(label="System",command=lambda: self.controller._set_appearance_mode("System")  , variable=self.controller.current_theme, value="System", accelerator=" ")
        appearance_menu.add_radiobutton(label="Light", command=lambda: self.controller._set_appearance_mode("Light") , variable=self.controller.current_theme, value="Light", accelerator=" ")
        appearance_menu.add_radiobutton(label="Dark", command=lambda: self.controller._set_appearance_mode("Dark")  , variable=self.controller.current_theme, value="Dark", accelerator=" ")
        

        view_menu.add_cascade(label="Appearance", menu=appearance_menu)

        view_menu.add_separator()
        view_menu.add_checkbutton(label="Show Sheet Panel",variable=self.controller.show_sheet_panel,
            command=self.controller.toggle_sheet_panel,onvalue=True,  offvalue=False)
        view_menu.add_checkbutton(
            label="Show Task Panel", variable=self.controller.show_task_panel,
            command=self.controller.toggle_task_panel, onvalue=True, offvalue=False)
        self.add_cascade(label="View", menu=view_menu)


    def _create_tools_menu(self):
        tools_menu = tk.Menu(self, tearoff=0)
        tools_menu.add_command(label="Polyspace Justifier", command=self.run_polyspace_justifier, accelerator="  F3")
        tools_menu.add_separator()
        tools_menu.add_command(label="Generate YDEMx", command=self._Not_implemented_yet, accelerator="  F4")
        tools_menu.add_command(label="Generate DEM", command=self._Not_implemented_yet, accelerator="  F5")
        tools_menu.add_command(label="Generate FIM", command=self._Not_implemented_yet, accelerator="  F6")
        tools_menu.add_command(label="Generate DTCH", command=self.run_dtch_generator, accelerator="  F7")
        self.add_cascade(label="Tools", menu=tools_menu)


    def _create_help_menu(self):
        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="About", command=self.controller._show_about_dialog, accelerator="F1")
        self.add_cascade(label="Help", menu=help_menu)


    def run_polyspace_justifier(self):
        PolyspaceApp(self.controller.root, self.controller)
        
    def run_dtch_generator(self):
         self.controller._generate_dtch()
        

    def _Not_implemented_yet(self):
        messagebox.showinfo( "Not Implemneted yet", "Not Implemneted yet" )