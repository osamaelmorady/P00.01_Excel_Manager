import customtkinter as ctk


class StatusBar(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, border_width=1)

        self.label = ctk.CTkLabel(
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

        self.label.configure(text="   |   ".join(parts))
