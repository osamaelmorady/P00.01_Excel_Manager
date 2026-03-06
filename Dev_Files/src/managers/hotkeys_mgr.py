"""
Centralized hotkey manager for the whole app.

All shortcuts defined here only.
"""


class HotkeyManager:

    def __init__(self, window):
        """
        window: MainWindow instance
        """
        self.window = window
        self.root = window.root

        self._bind_all()

    # =================================================
    # bindings
    # =================================================

    def _bind_all(self):

        # ---------- File ----------
        self._bind("<Control-n>", self.window.new_file)
        self._bind("<Control-o>", self.window.open_file)
        self._bind("<Control-s>", self.window.save_file)
        self._bind("<Control-Shift-s>", self.window.save_file_as) # ADD THIS LINE

        # ---------- Sheet ----------
        self._bind("<Control-t>", self.window.import_sheet)

        # ---------- Selection ----------
        self._bind("<Control-a>", self._select_all)
        self._bind("<Delete>", self._clear_cells)

        # ---------- Clipboard ----------
        self._bind("<Control-c>", self._copy)
        self._bind("<Control-v>", self._paste)
        self._bind("<Control-x>", self._cut)
        self._bind("<Control-z>", self._undo)
        self._bind("<Control-y>", self._redo)

    # =================================================
    # helpers
    # =================================================

    def _bind(self, key, func):
        self.root.bind_all(key, lambda e: func())

    def _view(self):
        return self.window.tabs.get_active_view()

    # =================================================
    # actions
    # =================================================

    def _new_sheet(self):
        name = self.window.manager._new_sheet()
        self.window.tabs.add_sheet(name, [[""]])
        # self.window.tabs.select("end-1")

    def _select_all(self):
        view = self._view()
        if view:
            view.sheet.select_all()

    def _clear_cells(self):
        view = self._view()
        if view:
            view.clear_selected_cells()

    def _copy(self):
        view = self._view()
        if view:
            view.sheet.copy()

    def _paste(self):
        view = self._view()
        if view:
            view.sheet.paste()

    def _cut(self):
        view = self._view()
        if view:
            view.sheet.cut()
            
    def _undo(self):
        view = self._view()
        if view:
            view.sheet.undo()

    def _redo(self):
        view = self._view()
        if view:
            view.sheet.redo()