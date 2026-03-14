"""
Auto Clipper Indonesia - Main Entry Point
Launch GUI application
"""

import customtkinter as ctk
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow


def main():
    """Main entry point for Auto Clipper Indonesia"""

    # CustomTkinter setup
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create main window
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()