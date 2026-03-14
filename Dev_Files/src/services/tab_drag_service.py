class TabDragService:

    def __init__(self, tabs):

        self.tabs = tabs

        self.drag_tab = None
        self.drag_index = None

    def bind(self):

        for btn in self.tabs.tab_bar._buttons_dict.values():

            btn.bind("<ButtonPress-1>", self.on_press)
            btn.bind("<B1-Motion>", self.on_drag)
            btn.bind("<ButtonRelease-1>", self.on_release)

    def _get_index(self, widget):

        buttons = list(self.tabs.tab_bar._buttons_dict.values())

        for i, btn in enumerate(buttons):

            if btn == widget:
                return i

        return None

    def on_press(self, event):

        idx = self._get_index(event.widget)

        if idx is None:
            return

        name = self.tabs.tab_names[idx]

        if name == "+":
            return

        self.drag_tab = name
        self.drag_index = idx

    def on_drag(self, event):

        if self.drag_tab is None:
            return

        new_idx = self._get_index(event.widget)

        if new_idx is None:
            return

        if new_idx == self.drag_index:
            return

        if self.tabs.tab_names[new_idx] == "+":
            return

        self.tabs.tab_names.insert(new_idx,
                                   self.tabs.tab_names.pop(self.drag_index))

        self.drag_index = new_idx

        self.tabs._refresh_tab_bar()

        self.tabs.tab_bar.set(self.drag_tab)

    def on_release(self, event):

        self.drag_tab = None
        self.drag_index = None