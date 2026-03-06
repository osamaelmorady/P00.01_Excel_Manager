# file_manager.py
import os
from tkinter import filedialog, messagebox


class FileManager:
    def __init__(self, main_window, csv_manager, sheet_tabs, app_state):
        self.main_window = main_window
        self.csv_manager = csv_manager
        self.csv_manager.sheet_tabs = sheet_tabs  # VERY IMPORTANT
        self.sheet_tabs = sheet_tabs
        self.app_state = app_state
        self.root = main_window.root  # Access the root from main_window

    def _update_title_bar(self, path=None):
        if path:
            self.main_window.root.title(f"Excel Manager - {path}")
        else:
            self.main_window.root.title("Excel Manager - New File")

    def new_file(self):
        # Check if there is a current sheet and ask to save
        if self.csv_manager.sheets:
            if messagebox.askyesno(
                "Save", "Do you want to save the current sheet before creating a new one?"
            ):
                self.save_file()

        # Clear the current sheet
        self.sheet_tabs.clear()
        self.csv_manager.sheets = {}
        self.csv_manager.path = None

        # Open a new sheet
        name = self.csv_manager._new_sheet()
        self.sheet_tabs.add_sheet(name, [[""]])
        self.sheet_tabs.select(0)
        self._update_title_bar()  # Update title bar for new file

    def open_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        self._open_path(path)


    def import_sheet(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return

        self.csv_manager.load(path)

        # Check if any sheets were loaded
        if not self.csv_manager.sheets:
            messagebox.showinfo("Info", "No data found in the selected file.")
            return

        # Use the filename without extension as the sheet name
        sheet_name = os.path.splitext(os.path.basename(path))[0]
        data = self.csv_manager.sheets["Sheet1"]  # csv always load to Sheet1, get the data from Sheet1
        del self.csv_manager.sheets["Sheet1"]  # delete the Sheet1
        self.csv_manager.sheets[sheet_name] = data  # save the sheet with filename

        # Check if the sheet name already exists in the *existing* sheets
        if sheet_name in self.sheet_tabs.views:
            # Generate a unique name for the imported sheet
            i = 1
            new_name = f"{sheet_name}_{i}"
            while new_name in self.sheet_tabs.views:
                i += 1
                new_name = f"{sheet_name}_{i}"
            sheet_name = new_name

        self.sheet_tabs.add_sheet(sheet_name, data)

        # Select the imported sheet
        # self.sheet_tabs.select(sheet_name)

        if not self.csv_manager.path:
            self.csv_manager.path = path  # Set the path if it's not already set


        # Select the imported sheet
        # self._update_title_bar()
        # self.sheet_tabs.select(sheet_name)







    def save_file(self):
        if self.csv_manager.path:
            self.csv_manager.sheets = self.sheet_tabs.get_all_data()
            self.csv_manager.save()
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
        self.csv_manager.path = path
        self.csv_manager.sheets = self.sheet_tabs.get_all_data()
        self.csv_manager.save(path)
        self._update_title_bar(path) # Update title bar

    def _open_path(self, path):
        self.csv_manager.load(path)

        self.sheet_tabs.clear()

        for name, data in self.csv_manager.sheets.items():
            self.sheet_tabs.add_sheet(name, data)

        self.sheet_tabs.select(0)
        self.app_state.save_last_path(path)
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
            name = self.csv_manager._new_sheet()
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
        name = self.csv_manager._new_sheet()
        self.sheet_tabs.add_sheet(name, [[""]])
