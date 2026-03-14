import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import re

class FimGenerator:
    def __init__(self, root, controller):
        self.top = ctk.CTkToplevel(root)
        self.root = self.top
        self.controller = controller  # Reference to the main application controller
        self.root.title("FIM Generator")
        self.root.geometry("800x500")  # Adjusted window size

        self.row_frames = []  # List to hold frames for each row

        self._build_gui()
        self.root.lift() #moving lift() to the end of build gui, to ensure it's called after the window is fully initialized
        self.root.focus_force()
        
    def _build_gui(self):
        # Main Frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)