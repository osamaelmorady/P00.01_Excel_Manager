import customtkinter as ctk
# from customtkinter.windows.ctk_toplevel import CTkMenu  # Import CTkMenu - REMOVE THIS LINE
from tksheet import Sheet
from tkinter import Menu  # Import Menu from tkinter
from services.formula_engine import FormulaEngine
from services.filter_engine import FilterEngine

class SheetView(ctk.CTkFrame):  # Inherit from ctk.CTkFrame

    def __init__(self, parent, status_bar=None):
        super().__init__(parent)
        self.formulas = {}
        self.original_data = []
        self.filtered_data = []
        self.active_filters = {}

        self.sheet = Sheet(self,
                           width=800,  # Set overall width
                           height=600,  # Set overall height
                           row_height=30,  # Set default row height
                           column_width=120)  # Set default column width

        self.sheet.pack(fill="both", expand=True)

        self.sheet.enable_bindings((
            "single_select",
            "row_select",
            "column_select",
            "drag_select",
            "arrowkeys",
            "edit_cell",

            # clipboard
            "copy",
            "cut",
            "paste",
            "delete",

            # advanced
            "undo",
            "redo",
            "select_all",
        ))

        self.sheet.extra_bindings([
            ("cell_select", self._update_status),
            ("drag_select_cells", self._update_status),
            ("edit_cell", self._on_cell_edit),
        ])

        self.status_bar = status_bar
        self._create_context_menu()

        # Enable manual resizing
        self.sheet.enable_bindings("column_width_resize")
        self.sheet.enable_bindings("row_height_resize")

    # --------------------------------
    # Context Menu
    # --------------------------------

    def _create_context_menu(self):
        menu = Menu(self, tearoff=0)  # Use tkinter.Menu

        menu.add_command(label="Add Row Above", command=self.add_row_above)
        menu.add_command(label="Add Row Below", command=self.add_row_below)

        menu.add_separator()

        menu.add_command(label="Add Column Left", command=self.add_col_left)
        menu.add_command(label="Add Column Right", command=self.add_col_right)

        menu.add_separator()

        menu.add_command(label="Delete Row", command=self.delete_row)
        menu.add_command(label="Delete Column", command=self.delete_col)

        self.sheet.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # --------------------------------
    # Row operations
    # --------------------------------

    def add_row_above(self):
        cells = self.sheet.get_selected_cells()
        if cells:
            r, _ = sorted(cells)[0]  # Get the row index of the first selected cell
        else:
            r = 0  # If no cell is selected, add at the beginning
        self.sheet.insert_row(idx=r)

    def add_row_below(self):
        cells = self.sheet.get_selected_cells()
        if cells:
            r, _ = sorted(cells)[0]  # Get the row index of the first selected cell
            r += 1
        else:
            r = self.sheet.get_total_rows()  # If no row selected, add at the end
        self.sheet.insert_row(idx=r)

    def delete_row(self):
        rows = sorted(self.sheet.get_selected_rows(), reverse=True)
        for r in rows:
            self.sheet.delete_row_position(r)

    # --------------------------------
    # Column operations
    # --------------------------------

    def add_col_left(self):
        cells = self.sheet.get_selected_cells()
        if cells:
            _, c = sorted(cells)[0]  # Get the column index of the first selected cell
        else:
            c = 0  # If no column is selected, add at the beginning
        self.sheet.insert_column(idx=c)

    def add_col_right(self):
        cells = self.sheet.get_selected_cells()
        if cells:
            _, c = sorted(cells)[0]  # Get the column index of the first selected cell
            c += 1
        else:
            c = self.sheet.get_total_columns()  # If no column is selected, add at the end
        self.sheet.insert_column(idx=c)

    def delete_col(self):
        cols = sorted(self.sheet.get_selected_columns(), reverse=True)
        for c in cols:
            self.sheet.delete_column_position(c)

    def clear_selected_cells(self):
        cells = self.sheet.get_selected_cells()

        for r, c in cells:
            self.sheet.set_cell_data(r, c, "")

    # --------------------------------
    # API
    # --------------------------------

    def load_data(self, data):

        self.engine = FilterEngine(data)

        self.sheet.set_sheet_data(data)

    def get_data(self):
        return self.sheet.get_sheet_data()

    # ---------------------------------
    # status bar integration
    # ---------------------------------

    def _update_status(self, event=None):

        if not self.status_bar:
            return

        cells = self.sheet.get_selected_cells()

        if not cells:
            return

        # convert set → ordered list
        cells = sorted(cells)

        r, c = cells[0]

        value = self.sheet.get_cell_data(r, c)

        cell_name = f"{self._col_name(c)}{r+1}"

        selection_size = len(cells)

        self.status_bar.update(
            cell=cell_name,
            value=value,
            selection=f"{selection_size} cells"
        )

    def _col_name(self, index):
        name = ""
        while True:
            index, r = divmod(index, 26)
            name = chr(65 + r) + name
            if index == 0:
                break
            index -= 1
        return name

    def _on_cell_edit(self, event=None):

        r = event.row
        c = event.column

        value = self.sheet.get_cell_data(r, c)

        if isinstance(value, str) and value.startswith("="):

            self.formulas[(r,c)] = value

            data = self.get_data()

            engine = FormulaEngine(data)

            result = engine.evaluate(value)

            self.sheet.set_cell_data(r, c, result)

        else:

            if (r,c) in self.formulas:
                del self.formulas[(r,c)]

        self._update_status()

    def evaluate_sheet(self):

        data = self.get_data()

        engine = FormulaEngine(data)

        evaluated = []

        for r,row in enumerate(data):

            new_row = []

            for c,cell in enumerate(row):

                if (r,c) in self.formulas:
                    new_row.append(engine.evaluate(self.formulas[(r,c)]))
                else:
                    new_row.append(cell)

            evaluated.append(new_row)

        return evaluated
    
    
    def apply_filter(self, column, value):

        filtered = self.engine.apply_filter(column, value)

        self.sheet.set_sheet_data(filtered)


    def clear_filters(self):

        data = self.engine.clear_filters()

        self.sheet.set_sheet_data(data)
        
        
        
    import tkinter as tk
    import customtkinter as ctk

    def open_filter_menu(self):
    
        cols = self.sheet.get_selected_columns()
    
        if not cols:
            return
    
        column = next(iter(cols))
    
        values = self.engine.unique_values(column)
    
        popup = ctk.CTkToplevel(self)
        popup.title("Filter Column")
    
        for value in values:
        
            btn = ctk.CTkButton(
                popup,
                text=str(value),
                command=lambda v=value: self.apply_filter(column, v)
            )
    
            btn.pack(fill="x", padx=10, pady=2)
    
        clear_btn = ctk.CTkButton(
            popup,
            text="Clear Filters",
            command=lambda: [self.clear_filters(), popup.destroy()]
        )
    
        clear_btn.pack(pady=10)