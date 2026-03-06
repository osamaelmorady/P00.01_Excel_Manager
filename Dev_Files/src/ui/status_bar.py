import tkinter as tk


class StatusBar(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bd=1, relief="sunken")

        self.label = tk.Label(
            self,
            text="Ready",
            anchor="w",
            padx=10
        )
        self.label.pack(fill="x")

    # ---------------------------------
    # public API
    # ---------------------------------

    def update(self, cell=None, value=None, sheet=None, selection=None):

        parts = []

        if sheet:
            parts.append(f"Sheet: {sheet}")

        if cell:
            parts.append(f"Cell: {cell}")

        if value is not None:
            parts.append(f"Value: {value}")

        if selection:
            parts.append(f"Selected: {selection}")

        self.label.config(text="   |   ".join(parts))
