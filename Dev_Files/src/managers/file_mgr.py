# file_mgr.py
import os
from tkinter import filedialog, messagebox
from managers.Sheets_mgr import SheetsManager


class FileManager:
    def __init__(self, main_window, sheet_tabs, app_state):
        self.main_window = main_window
        # self.csv_manager = csv_manager # Remove csv_manager
        self.sheet_tabs = sheet_tabs
        self.app_state = app_state
        self.root = main_window.root  # Access the root from main_window
        self.sheets_manager = SheetsManager()  # Initialize SheetsManager here
        self.path = None

    def _update_title_bar(self, path=None):
        if path:
            self.main_window.root.title(f"Excel Manager - {path}")
        else:
            self.main_window.root.title("Excel Manager - New File")

    def new_file(self):
        # Check if there is a current sheet and ask to save
        if self.sheets_manager.sheets:
            if messagebox.askyesno(
                "Save",
                "Do you want to save the current sheet before creating a new one?",
            ):
                self.save_file()

        # Clear the current sheet
        self.sheet_tabs.clear()
        self.sheets_manager.sheets = {}
        self.path = None

        # Open a new sheet
        name = self.sheets_manager.new_sheet()
        self.sheet_tabs.add_sheet(name, [[""]])
        # self.sheet_tabs.select(0)
        self._update_title_bar()  # Update title bar for new file

    def open_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        self._open_path(path)

    def _open_path(self, path):

        ext = os.path.splitext(path)[1].lower()
        file_name_without_ext = os.path.splitext(os.path.basename(path))[0]

        # clear tabs
        self.sheet_tabs.clear()

        if ext == ".csv":

            self.sheets_manager.load_csv(path)

            if "Sheet1" in self.sheets_manager.sheets:
                data = self.sheets_manager.sheets.pop("Sheet1")
                self.sheets_manager.sheets[file_name_without_ext] = data

        elif ext == ".xlsx":

            self.sheets_manager.load_excel(path)

        else:
            messagebox.showerror("Error", "Unsupported file type.")
            return

        # ------------------------------------------------
        # Load sheets into UI
        # ------------------------------------------------
        for name, data in self.sheets_manager.sheets.items():

            original_name = name
            i = 1

            while name in self.sheet_tabs.tab_names:
                name = f"{original_name}_{i}"
                i += 1

            self.sheet_tabs.add_sheet(name, data)

        # ------------------------------------------------
        # Select first sheet
        # ------------------------------------------------
        if self.sheets_manager.sheets:

            first_sheet_name = next(iter(self.sheets_manager.sheets))

            self.sheet_tabs.tab_bar.set(first_sheet_name)
            self.sheet_tabs._show_frame(first_sheet_name)

        self.app_state.save_last_path(path)
        self._update_title_bar(path)

        self.path = path



    def import_sheet(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return

        result = self.sheets_manager.import_sheet(path, self.sheet_tabs)

        if not result:
            messagebox.showinfo("Info", "No data found in the selected file.")
            return

        sheet_name, data = result

        self.sheet_tabs.add_sheet(sheet_name, data)

        # Select the imported sheet
        # self.sheet_tabs.select(sheet_name)

        if not self.path:
            self.path = path  # Set the path if it's not already set

        # Select the imported sheet
        # self._update_title_bar()
        # self.sheet_tabs.select(sheet_name)

    def save_file(self):
        if self.path:
            # self.csv_manager.sheets = self.sheet_tabs.get_all_data()
            ext = os.path.splitext(self.path)[1].lower()
            self.sheets_manager.sheets = self.sheet_tabs.get_all_data()

            if ext == ".csv":
                active_view = self.sheet_tabs.get_active_view()
                if active_view:
                    # active_sheet_name = self.sheet_tabs.tab(active_view.master, "text") #old
                    active_sheet_name = self.sheet_tabs.tab_bar.get() #new
                    self.sheets_manager.save_csv(self.path, active_sheet_name)
                else:
                    print("No active sheet found.")  # Handle the case where there's no active sheet
            else:
                self.sheets_manager.save_excel(self.path)
        else:
            self.save_file_as()


    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".*",
            filetypes=[
                ("CSV file", "*.csv"),
                ("Excel file", "*.xlsx"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        ext = os.path.splitext(path)[1].lower()
        self.sheets_manager.sheets = self.sheet_tabs.get_all_data()

        if ext == ".csv":
            active_view = self.sheet_tabs.get_active_view()
            if active_view:
                # active_sheet_name = self.sheet_tabs.tab(active_view.master, "text") #old
                active_sheet_name = self.sheet_tabs.tab_bar.get() #new
                self.sheets_manager.save_csv(path, active_sheet_name)
            else:
                print("No active sheet found.")  # Handle the case where there's no active sheet
        else:
            self.sheets_manager.save_excel(path)

        self.path = path
        self._update_title_bar(path)  # Update title bar


    def on_drop(self, event):
        path = event.data.strip("{}")  # windows path fix
        if os.path.isfile(path):
            self._open_path(path)

    def load_last_session(self):
        path = self.app_state.load_last_path()

        if path and os.path.exists(path):
            self._open_path(path)
        else:
            # first time → empty sheet
            name = self.sheets_manager.new_sheet()
            self.sheet_tabs.add_sheet(name, [[""]])

    def startup_load(self, startup_file):  # Pass startup_file
        # 1) file dropped on exe
        if startup_file:
            self._open_path(startup_file)
            return

        # 2) last session
        last = self.app_state.load_last_path()
        if last and os.path.exists(last):
            self._open_path(last)
            return

        # 3) empty sheet
        name = self.sheets_manager.new_sheet()
        self.sheet_tabs.add_sheet(name, [[""]])
