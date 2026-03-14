# ui/polyspace_justifier.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd


class PolyspaceApp:
    def __init__(self, root, controller):
        self.top = ctk.CTkToplevel(root)
        self.root = self.top
        self.controller = controller  # Reference to the main application controller
        self.root.title("Polyspace Justifier")
        self.root.geometry("800x500")  # Adjusted window size

        self.row_frames = []  # List to hold frames for each row

        self._build_gui()
        self.root.lift() #moving lift() to the end of build gui, to ensure it's called after the window is fully initialized
        self.root.focus_force()

    def _build_gui(self):
        # Main Frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # + Button (Top Left)
        add_button = ctk.CTkButton(main_frame, text="+", command=self._add_row)
        add_button.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        # Frame for Rows
        self.rows_frame = ctk.CTkFrame(main_frame)
        self.rows_frame.grid(row=1, column=0, sticky="nsew")

        # Initial row
        self._add_row()

        # Run Button (Bottom Right)
        run_button = ctk.CTkButton(main_frame, text="Run", command=self._run_justifier)
        run_button.grid(row=2, column=0, sticky="se", padx=5, pady=5)

        # Configure grid layout
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def _add_row(self):
        # Separator Line
        separator = ctk.CTkFrame(self.rows_frame, height=2)
        separator.configure(fg_color="lightgray")
        separator.pack(fill="x", pady=5)

        row_frame = ctk.CTkFrame(self.rows_frame)
        row_frame.pack(fill="x", padx=30, pady=5)

        # Old CSV Line
        old_frame = ctk.CTkFrame(row_frame)
        old_frame.pack(fill="x", padx=30, pady=2)

        old_label = ctk.CTkLabel(old_frame, text="Old CSV:")
        old_label.pack(side=ctk.LEFT, padx=5)
        old_browse_button = ctk.CTkButton(old_frame, text="Browse",
                                       command=lambda rf=old_frame, csv_type="old": self._browse_sheet(rf, csv_type))
        old_browse_button.pack(side=ctk.LEFT, padx=5)
        old_sheet_var = ctk.StringVar()
        #old_sheet_label = tk.Label(old_frame, textvariable=old_sheet_var, width=40)  # Use Label instead of Entry
        #old_sheet_label.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        old_sheet_entry = ctk.CTkEntry(old_frame, textvariable=old_sheet_var, width=40)
        old_sheet_entry.pack(side=ctk.LEFT, fill="x", expand=True, padx=5)

        # Add Input Textbox to Old CSV Line
        input_label_old = ctk.CTkLabel(old_frame, text="Reference attributes")
        input_label_old.pack(side=ctk.LEFT, padx=5)
        input_var_old = ctk.StringVar()
        input_entry_old = ctk.CTkEntry(old_frame, textvariable=input_var_old, width=50)  # Increased width here
        input_entry_old.pack(side=ctk.LEFT, fill="x", expand=True, padx=5)
        #input_entry_old.config(width=50) #no config for ctk

        # New CSV Line
        new_frame = ctk.CTkFrame(row_frame)
        new_frame.pack(fill="x", padx=30, pady=2)

        new_label = ctk.CTkLabel(new_frame, text="New CSV:")
        new_label.pack(side=ctk.LEFT, padx=5)
        new_browse_button = ctk.CTkButton(new_frame, text="Browse",
                                       command=lambda rf=new_frame, csv_type="new": self._browse_sheet(rf, csv_type))
        new_browse_button.pack(side=ctk.LEFT, padx=5)
        new_sheet_var = ctk.StringVar()
        #new_sheet_label = tk.Label(new_frame, textvariable=new_sheet_var, width=40)  # Use Label instead of Entry
        #new_sheet_label.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        new_sheet_entry = ctk.CTkEntry(new_frame, textvariable=new_sheet_var, width=40)
        new_sheet_entry.pack(side=ctk.LEFT, fill="x", expand=True, padx=5)

        # Add Input Textbox
        input_label = ctk.CTkLabel(new_frame, text="Updated attributes")
        input_label.pack(side=ctk.LEFT, padx=5)
        input_var = ctk.StringVar()
        input_entry = ctk.CTkEntry(new_frame, textvariable=input_var, width=50)  # Increased width here
        input_entry.pack(side=ctk.LEFT, fill="x", expand=True, padx=5)
        #input_entry.config(width=50) #no config for ctk

        # Run Button for this Row
        run_row_button = ctk.CTkButton(row_frame, text="Run Row",
                                        command=lambda rf=row_frame: self._run_justifier_for_row(rf))
        run_row_button.pack(side=ctk.RIGHT, padx=5)

        self.row_frames.append({
            'frame': row_frame,
            'old_sheet_var': old_sheet_var,
            'new_sheet_var': new_sheet_var,
            'input_var': input_var,
            'input_var_old': input_var_old
        })  # Store the frame, vars


    



    def _browse_sheet(self, row_frame, csv_type):
        sheet_names = list(self.controller.manager.sheets.keys())
        
        print (sheet_names)
        if not sheet_names:
            messagebox.showinfo("Info", "No sheets available.")
            return

        sheet_name = ctk.StringVar(value=sheet_names[0])  # Default to first sheet

        popup = ctk.CTkToplevel(self.root)
        popup.title(f"Select {csv_type.capitalize()} CSV Sheet")

        label = ctk.CTkLabel(popup, text=f"Select {csv_type.capitalize()} CSV Sheet:")
        label.pack(pady=5)
        
        sheet_dropdown = ctk.CTkComboBox(popup, values = sheet_names, variable=sheet_name)
        
        print (sheet_name)
        sheet_dropdown.pack(pady=5)

        def set_sheet(sheet_name = sheet_name, target_vars = self.row_frames):
            # Find the label in the row and set the value
            if csv_type == "old":
                target_var = next((rf['old_sheet_var'] for rf in self.row_frames if rf['frame'] == row_frame), None)
            else:
                target_var = next((rf['new_sheet_var'] for rf in self.row_frames if rf['frame'] == row_frame), None)

            if target_var:
                target_var.set(sheet_name.get())
            popup.destroy()

        select_button = ctk.CTkButton(popup, text="Select", command=set_sheet)
        select_button.pack(pady=5)






    def _run_justifier(self):
        # collect all old and new sheets,
        old_sheets = []
        new_sheets = []
        inputs = []
        inputs_old = []

        for row_data in self.row_frames:
            row_frame = row_data['frame']
            old_sheet_name = row_data['old_sheet_var'].get()
            new_sheet_name = row_data['new_sheet_var'].get()
            input_value = row_data['input_var'].get()
            input_value_old = row_data['input_var_old'].get()

            if not old_sheet_name or not new_sheet_name or not input_value or not input_value_old:
                messagebox.showerror("Error", "Please fill in all sheet names and input.")
                return

            if old_sheet_name not in self.controller.manager.sheets or new_sheet_name not in self.controller.manager.sheets:
                messagebox.showerror("Error", "One or more input sheets not found.")
                return
            
            old_sheets.append(self.controller.manager.sheets[old_sheet_name])
            new_sheets.append(self.controller.manager.sheets[new_sheet_name])
            inputs.append(input_value)
            inputs_old.append(input_value_old)


        messagebox.showinfo("Success", "Polyspace justification complete!")


    def _update_data(self, old_data, new_data):
        """
        Copies justification data from old_data to new_data based on matching
        columns and updates specified columns.
        """
        old_df = pd.DataFrame(old_data, columns=old_data[0])  # Assuming first row is header
        new_df = pd.DataFrame(new_data, columns=new_data[0])

        # Ensure match_cols exist in both DataFrames
        missing_match_cols = set(self.match_cols) - set(old_df.columns) - set(new_df.columns)
        if missing_match_cols:
            raise ValueError(f"Missing match columns: {missing_match_cols}")
    
        # Ensure update_cols exist in old_df
        missing_update_cols = set(self.update_cols) - set(old_df.columns)
        if missing_update_cols:
            raise ValueError(f"Missing update columns: {missing_update_cols}")

        # Create a lookup from the old DataFrame
        lookup = old_df.set_index(self.match_cols)[self.update_cols].to_dict('index')
    
        def update_row(row):
            try:
                key = tuple(row[col] for col in self.match_cols)
                if key in lookup:
                    for col in self.update_cols:
                        row[col] = lookup[key][col]
            except KeyError as e:
                print(f"KeyError: {e}")  # Handle missing columns in the row
            return row
    
        # Apply the update row-wise
        new_df = new_df.apply(update_row, axis=1)

        return new_df.values.tolist()


    def _run_justifier_for_row(self, row_frame):
        """Runs the polyspace justification for a specific row."""
        row_data = next((row for row in self.row_frames if row['frame'] == row_frame), None)
        if not row_data:
            messagebox.showerror("Error", "Row data not found.")
            return
    
        old_sheet_name = row_data['old_sheet_var'].get()
        new_sheet_name = row_data['new_sheet_var'].get()
        input_value = row_data['input_var'].get()
        input_value_old = row_data['input_var_old'].get()
    
        if not old_sheet_name or not new_sheet_name or not input_value or not input_value_old:
            messagebox.showerror("Error", "Please fill in all sheet names and input.")
            return
    
        if old_sheet_name not in self.controller.manager.sheets or new_sheet_name not in self.controller.manager.sheets:
            messagebox.showerror("Error", "One or more input sheets not found.")
            return
    
        old_data = self.controller.manager.sheets[old_sheet_name]
        new_data = self.controller.manager.sheets[new_sheet_name]
    
        # Add your justification logic here, using old_data, new_data, input_value, and input_value_old
        # For example:
        try:
            #result = self._update_data(old_data, new_data)  # Pass the data to the function
            #messagebox.showinfo("Success", "Polyspace justification complete for this row!")
            messagebox.showinfo("Success", f"Polyspace justification complete for this row with {old_sheet_name} and {new_sheet_name}!")
        except Exception as e:
            messagebox.showerror("Error", f"Polyspace justification failed: {e}")
