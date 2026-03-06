import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ui.sheet_view import SheetView


class SheetTabs(ttk.Notebook):

    def __init__(self, parent, manager, status_bar):
        super().__init__(parent)

        self.manager = manager
        self.views = {}
        self._loading = False

        self.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self.bind("<Button-3>", self._show_tab_menu)

        self._create_plus_tab()
        self.status_bar = status_bar

    # =================================================
    # "+" tab
    # =================================================

    def _create_plus_tab(self):
        frame = tk.Frame(self)
        self.add(frame, text="  +  ")

    def _on_tab_changed(self, event):
    
        # ignore during loading
        if self._loading:
            return
    
        idx = self.index("current")
    
        if idx == len(self.tabs()) - 1:  # "+" clicked
            name = self.manager._new_sheet()
            self.add_sheet(name, self.manager.sheets[name])
            self.select(len(self.tabs()) - 2)


    # =================================================
    # context menu
    # =================================================

    def _show_tab_menu(self, event):
        try:
            idx = self.index(f"@{event.x},{event.y}")
        except:
            return

        # ignore "+" tab
        if idx == len(self.tabs()) - 1:
            return

        menu = tk.Menu(self, tearoff=0)

        menu.add_command(label="Rename", command=lambda: self.rename_sheet(idx))
        menu.add_command(label="Duplicate", command=lambda: self.duplicate_sheet(idx))
        menu.add_separator()
        menu.add_command(label="Move Left", command=lambda: self.move_left(idx))
        menu.add_command(label="Move Right", command=lambda: self.move_right(idx))
        menu.add_separator()
        menu.add_command(label="Delete", command=lambda: self.delete_sheet(idx))

        menu.tk_popup(event.x_root, event.y_root)

    # =================================================
    # operations
    # =================================================

    def rename_sheet(self, idx):
        old_name = self.tab(idx, "text")

        new_name = simpledialog.askstring("Rename Sheet", "New name:", initialvalue=old_name)
        if not new_name:
            return

        if new_name in self.manager.sheets:
            messagebox.showerror("Error", "Sheet name already exists.")
            return

        self.manager.sheets[new_name] = self.manager.sheets.pop(old_name)
        self.views[new_name] = self.views.pop(old_name)

        self.tab(idx, text=new_name)

    # -------------------------------------------------

    def duplicate_sheet(self, idx):
        name = self.tab(idx, "text")
        data = self.views[name].get_data()

        new_name = self.manager._new_sheet(f"{name}_copy")

        self.manager.sheets[new_name] = [row[:] for row in data]
        self.add_sheet(new_name, self.manager.sheets[new_name])

    # -------------------------------------------------

    def delete_sheet(self, idx):
        name = self.tab(idx, "text")

        total_sheets = len(self.views)

        # -------------------------------------------------
        # Case 1: more than one sheet
        # -------------------------------------------------
        if total_sheets > 1:
            del self.manager.sheets[name]
            del self.views[name]

            self.forget(idx)

            # switch to previous tab if possible
            new_idx = max(0, idx - 1)
            self.select(new_idx)

        # -------------------------------------------------
        # Case 2: last remaining sheet
        # -------------------------------------------------
        else:
            # clear data instead of removing
            self.views[name].load_data([[""]])
            self.manager.sheets[name] = [[""]]


    # -------------------------------------------------

    def move_left(self, idx):
        if idx <= 0:
            return
        self.insert(idx - 1, self.tabs()[idx])

    def move_right(self, idx):
        if idx >= len(self.tabs()) - 2:
            return
        self.insert(idx + 1, self.tabs()[idx])

    # =================================================
    # public API
    # =================================================

    def clear(self):
        self._loading = True

        for tab in self.tabs():
            self.forget(tab)

        self.views.clear()
        self._create_plus_tab()

        self._loading = False


    def add_sheet(self, name, data):
        frame = tk.Frame(self)

        view = SheetView(frame, self.status_bar)
        view.pack(fill="both", expand=True)
        view.load_data(data)

        self.views[name] = view

        self.insert(len(self.tabs()) - 1, frame, text=name)

    def get_all_data(self):
        return {
            name: view.get_data()
            for name, view in self.views.items()
        }


    def get_active_view(self):
        tab_id = self.select()
        frame = self.nametowidget(tab_id)

        for view in self.views.values():
            if view.master == frame:
                return view

        return None
