import customtkinter as ctk
from tkinter import simpledialog, messagebox, Menu
from ui.sheet_view import SheetView
from services.tab_drag_service import TabDragService
from services.scrollable_tab_bar import ScrollableTabBar


class SheetTabs(ctk.CTkFrame):

    def __init__(self, parent, manager, status_bar):
        super().__init__(parent)

        self.manager = manager
        self.status_bar = status_bar

        self.views = {}
        self.tab_frames = {}
        self.tab_names = []
        self._loading = False


        # Layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ------------------------------------------------
        # Tab bar
        # ------------------------------------------------
        self.tab_bar = ctk.CTkSegmentedButton(
            self,
            values=[],
            command=self._tab_selected
        )
        self.tab_bar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)


        
        # Tab actions button
        self.menu_button = ctk.CTkButton(
            self,
            text="⋮",
            width=30,
            command=self._show_tab_menu
        )
        self.menu_button.grid(row=0, column=1, padx=5)


        # ------------------------------------------------
        # Tab bar features
        # ------------------------------------------------
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        # self.tab_bar = ScrollableTabBar(self, command=self._tab_selected)
        # self.tab_bar.grid(row=0, column=0, sticky="ew")
        
        # self.drag_service = TabDragService(self)
        # ------------------------------------------------
        # Content container
        # ------------------------------------------------
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # ------------------------------------------------
        # Context menu
        # ------------------------------------------------
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label="Rename", command=self.rename_current)
        self.menu.add_command(label="Duplicate", command=self.duplicate_current)
        self.menu.add_separator()
        self.menu.add_command(label="Move Left", command=self.move_left_current)
        self.menu.add_command(label="Move Right", command=self.move_right_current)
        self.menu.add_separator()
        self.menu.add_command(label="Delete", command=self.delete_current)

        # create "+" tab
        self._create_plus_tab()

    # =====================================================
    # Tabs
    # =====================================================

    def _create_plus_tab(self):

        self.tab_names.append("+")
        self._refresh_tab_bar()

    def _refresh_tab_bar(self):
        self.tab_names = list(dict.fromkeys(self.tab_names))
        self.tab_bar.configure(values=self.tab_names)
        
        # self.tab_bar.set_tabs(self.tab_names)
        # self.after(10, self.drag_service.bind)

    def _generate_unique_name(self, name):

        if name not in self.tab_names:
            return name

        i = 1
        new_name = f"{name}_{i}"

        while new_name in self.tab_names:
            i += 1
            new_name = f"{name}_{i}"

        return new_name


    def add_sheet(self, name, data):

        if "+" in self.tab_names:
            self.tab_names.remove("+")

        name = self._generate_unique_name(name)
        self.tab_names.append(name)
        self.tab_names.append("+")

        frame = ctk.CTkFrame(self.content)

        view = SheetView(frame, self.status_bar)
        view.pack(fill="both", expand=True)
        view.load_data(data)

        self.views[name] = view
        self.tab_frames[name] = frame

        self._refresh_tab_bar()
        self.tab_bar.set(name)

        self._show_frame(name)

    # =====================================================
    # Tab switching
    # =====================================================

    def _tab_selected(self, tab_name):

        if self._loading:
            return

        if tab_name == "+":
            name = self.manager.new_sheet()
            self.add_sheet(name, self.manager.sheets[name])
            return

        self._show_frame(tab_name)

    def _show_frame(self, name):

        for frame in self.tab_frames.values():
            frame.pack_forget()

        frame = self.tab_frames.get(name)

        if frame:
            frame.pack(fill="both", expand=True)

    # =====================================================
    # Context menu
    # =====================================================

    def _show_tab_menu(self):

        current = self.tab_bar.get()

        if current == "+":
            return

        self._context_tab = current

        x = self.menu_button.winfo_rootx()
        y = self.menu_button.winfo_rooty() + self.menu_button.winfo_height()

        self.menu.tk_popup(x, y)

    # =====================================================
    # Operations
    # =====================================================

    def rename_current(self):

        old = self._context_tab

        new = simpledialog.askstring(
            "Rename Sheet",
            "New name:",
            initialvalue=old
        )

        if not new:
            return

        if new in self.views:
            messagebox.showerror("Error", "Sheet already exists.")
            return

        data = self.views[old].get_data()

        self.delete_sheet(old)
        self.add_sheet(new, data)

    def duplicate_current(self):

        name = self._context_tab
        data = self.views[name].get_data()

        new_name = self.manager.new_sheet(f"{name}_copy")

        self.manager.sheets[new_name] = [row[:] for row in data]

        self.add_sheet(new_name, self.manager.sheets[new_name])

    def delete_current(self):

        self.delete_sheet(self._context_tab)

    def delete_sheet(self, name):

        if len(self.views) <= 1:

            self.views[name].load_data([[""]])
            self.manager.sheets[name] = [[""]]
            return

        self.tab_frames[name].destroy()

        del self.views[name]
        del self.tab_frames[name]
        del self.manager.sheets[name]

        self.tab_names.remove(name)

        self._refresh_tab_bar()

        if self.tab_names:
            self.tab_bar.set(self.tab_names[0])
            self._show_frame(self.tab_names[0])

    # =====================================================
    # Move operations
    # =====================================================

    def move_left_current(self):

        name = self._context_tab
        idx = self.tab_names.index(name)

        if idx == 0:
            return

        self.tab_names[idx], self.tab_names[idx-1] = (
            self.tab_names[idx-1],
            self.tab_names[idx]
        )

        self._refresh_tab_bar()
        self.tab_bar.set(name)

    def move_right_current(self):

        name = self._context_tab
        idx = self.tab_names.index(name)

        if idx >= len(self.tab_names) - 2:
            return

        self.tab_names[idx], self.tab_names[idx+1] = (
            self.tab_names[idx+1],
            self.tab_names[idx]
        )

        self._refresh_tab_bar()
        self.tab_bar.set(name)

    # =====================================================
    # API
    # =====================================================

    def clear(self):

        self._loading = True

        for frame in self.tab_frames.values():
            frame.destroy()

        self.views.clear()
        self.tab_frames.clear()
        self.tab_names.clear()

        self._create_plus_tab()

        self._loading = False

    def get_active_view(self):
        """
        Return the currently active sheet view.
        """
        current = self.tab_bar.get()

        return self.views.get(current)
    
    
    def get_all_data(self):
        """
        Collect all spreadsheet data from every sheet view.
        Returns a dictionary: {sheet_name: data}
        """
        all_data = {}

        for name, view in self.views.items():
            try:
                all_data[name] = view.get_data()
            except Exception:
                all_data[name] = [[""]]

        return all_data