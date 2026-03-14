# src/generate_dtch.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import re

class DtchGenerator:
    def __init__(self, root, controller):
        self.top = ctk.CTkToplevel(root)
        self.root = self.top
        self.controller = controller  # Reference to the main application controller
        self.root.title("DTCH Generator")
        self.root.geometry("800x500")  # Adjusted window size

        self.row_frames = []  # List to hold frames for each row

        self._build_gui()
        self.root.lift() #moving lift() to the end of build gui, to ensure it's called after the window is fully initialized
        self.root.focus_force()
        
    def _build_gui(self):
        # Main Frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        
        
    def process_dtch_data(self, data):
        """
        Processes DTCH data directly from the sheet content.
        """

        def sanitize_c_identifier(name_str):
            if not isinstance(name_str, str):
                return ""
            return re.sub(r'[^a-zA-Z0-9_]', '_', name_str)

        def convert_dtc_format(dtc_str):
            if not isinstance(dtc_str, str) or len(dtc_str) < 2:
                return dtc_str.lower() if isinstance(dtc_str, str) else dtc_str
            prefix = dtc_str[0].upper()
            digit = dtc_str[1]
            rest = dtc_str[2:]
            hex_prefix = ""
            try:
                digit_val = int(digit)
                if prefix == 'P':
                    hex_prefix = hex(0x0 + digit_val)[2:]
                elif prefix == 'C':
                    hex_prefix = hex(0x4 + digit_val)[2:]
                elif prefix == 'B':
                    hex_prefix = hex(0x8 + digit_val)[2:]
                elif prefix == 'U':
                    hex_prefix = hex(0xC + digit_val)[2:]
                else:
                    return dtc_str.lower()
                return f"0x{hex_prefix}{rest}".lower()
            except ValueError:
                return dtc_str.lower()
            except Exception:
                return dtc_str.lower()

        def _max_e_count(df):
            m = 0
            for c in range(1, len(df.columns)):
                cnt = 0
                for r in range(1, len(df)):
                    v = df.iloc[r, c]
                    if isinstance(v, str) and v.strip().lower() == 'e':
                        cnt += 1
                if cnt > m:
                    m = cnt
            return m

        # Convert data to DataFrame
        df = pd.DataFrame(data)

        # --- Step 1: Convert header row (Row index 0) ---
        for col_idx in range(1, len(df.columns)):
            if df.iloc[0, col_idx] is not None:
                dtc_hex = convert_dtc_format(str(df.iloc[0, col_idx]))
                df.iloc[0, col_idx] = dtc_hex

        output_lines = []
        line = f"/*     DTC entries     */"
        output_lines.append(line)

        for col_idx in range(1, len(df.columns)):
            if df.iloc[1, col_idx] is not None:
                dtc_hex_code = str(df.iloc[1, col_idx])  # Ensure it's a string

                defects_list = []
                dtc_name_list = []
                dtc_name_list.append(f"{df.iloc[0, col_idx]}")

                for row_idx in range(2, len(df)):
                    cell_value = df.iloc[row_idx, col_idx]

                    if isinstance(cell_value, str) and cell_value.lower() == 'e':
                        defect_name_raw = df.iloc[row_idx, 0]
                        defect_name_sanitized = sanitize_c_identifier(defect_name_raw)
                        defects_list.append(f"u16YDEMx_{defect_name_sanitized}")

                x_count = len(defects_list)

                if x_count >= 0:
                    defects_str = ", ".join(defects_list + ["u16YDEMx_Invalid_Event"] * max(0, _max_e_count(df) - len(defects_list)))
                    line = f"/* {dtc_name_list}\t\t */ {{DTCH_{dtc_hex_code}, {{{defects_str}}}, DTC_STATUS_PREPASSED, {x_count}U}},"
                    output_lines.append(line)

        line_count = len(output_lines)
        output = f"#define DTCH_U8_DTCS_NUM    ((u8){line_count-1})\n\n"
        output += "\n".join(output_lines)
        return output
