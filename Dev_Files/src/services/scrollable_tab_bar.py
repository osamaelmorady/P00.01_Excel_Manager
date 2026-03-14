import customtkinter as ctk
import tkinter as tk


class ScrollableTabBar(ctk.CTkFrame):

    def __init__(self, parent, command=None):
        super().__init__(parent)

        self.command = command

        self.canvas = tk.Canvas(self, height=40, highlightthickness=0)
        self.canvas.pack(side="top", fill="x", expand=True)

        self.scrollbar = tk.Scrollbar(
            self,
            orient="horizontal",
            command=self.canvas.xview
        )
        self.scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.inner_frame = ctk.CTkFrame(self.canvas)

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.inner_frame,
            anchor="nw"
        )

        self.inner_frame.bind("<Configure>", self._update_scrollregion)

        self.tab_bar = ctk.CTkSegmentedButton(
            self.inner_frame,
            values=[],
            command=self._on_tab_selected
        )

        self.tab_bar.pack(fill="x", expand=True)

    def _update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_tab_selected(self, value):

        if self.command:
            self.command(value)

    # API

    def set_tabs(self, names):
        self.tab_bar.configure(values=names)

    def set(self, name):
        self.tab_bar.set(name)

    def get(self):
        return self.tab_bar.get()

    @property
    def buttons(self):
        return self.tab_bar._buttons_dict