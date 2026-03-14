"""
Auto Clipper Indonesia - Export Panel
Export progress and file management
"""

import customtkinter as ctk


def create_export_panel(parent_frame, main_window):
    """Create the export progress panel"""

    # Header
    header_label = ctk.CTkLabel(
        parent_frame,
        text="Export Progress",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    header_label.pack(pady=10)

    # Export list frame
    export_frame = ctk.CTkScrollableFrame(parent_frame, height=400)
    export_frame.pack(fill="x", padx=20, pady=10)

    # Overall progress
    progress_frame = ctk.CTkFrame(parent_frame)
    progress_frame.pack(fill="x", padx=20, pady=10)

    overall_label = ctk.CTkLabel(
        progress_frame,
        text="Overall Progress:",
        font=ctk.CTkFont(size=14)
    )
    overall_label.pack(side="left", padx=10, pady=10)

    overall_progress = ctk.CTkProgressBar(progress_frame)
    overall_progress.set(0)
    overall_progress.pack(side="left", padx=10, pady=10)

    overall_percent = ctk.CTkLabel(
        progress_frame,
        text="0%"
    )
    overall_percent.pack(side="left", padx=5, pady=10)

    # Buttons
    button_frame = ctk.CTkFrame(parent_frame)
    button_frame.pack(fill="x", padx=20, pady=10)

    open_folder_button = ctk.CTkButton(
        button_frame,
        text="Open Output Folder",
        height=40,
        width=200,
        command=lambda: open_output_folder()
    )
    open_folder_button.pack(side="left", padx=5, pady=5)

    new_video_button = ctk.CTkButton(
        button_frame,
        text="Upload New Video",
        height=40,
        width=200,
        command=lambda: main_window.tabview.set("Upload")
    )
    new_video_button.pack(side="left", padx=5, pady=5)

    return export_frame


def update_export_list(export_frame, exports):
    """Update the export list with exported clips"""
    for widget in export_frame.winfo_children():
        widget.destroy()

    if not exports:
        no_exports_label = ctk.CTkLabel(
            export_frame,
            text="No exports yet. Select clips and export.",
            text_color="gray"
        )
        no_exports_label.pack(pady=20)
        return

    for i, export in enumerate(exports):
        clip_frame = ctk.CTkFrame(export_frame)
        clip_frame.pack(fill="x", padx=5, pady=5)

        filename_label = ctk.CTkLabel(
            clip_frame,
            text=f"{export['filename']}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        filename_label.pack(side="left", padx=10, pady=5)

        status_label = ctk.CTkLabel(
            clip_frame,
            text=f"Status: {export['status']}",
            text_color="green" if export['status'] == "Complete" else "yellow"
        )
        status_label.pack(side="left", padx=10, pady=5)

        size_label = ctk.CTkLabel(
            clip_frame,
            text=f"{export['size']}",
            text_color="gray"
        )
        size_label.pack(side="left", padx=10, pady=5)


def open_output_folder():
    """Open the output video folder"""
    import os
    import subprocess
    import pathlib

    output_dir = pathlib.Path(__file__).parent.parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if os.name == 'nt':  # Windows
        os.startfile(str(output_dir))
    elif os.name == 'posix':
        subprocess.run(['open', str(output_dir)])


if __name__ == "__main__":
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    from gui.main_window import MainWindow

    import customtkinter as ctk

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1200x800")

    test_frame = ctk.CTkFrame(root)
    test_frame.pack(fill="both", expand=True)

    main_window = MainWindow()

    export_frame = create_export_panel(test_frame, main_window)

    export_list = [
        {"filename": "clip_001.mp4", "status": "Complete", "size": "25MB"},
        {"filename": "clip_002.mp4", "status": "Complete", "size": "23MB"},
    ]

    update_export_list(export_frame, export_list)

    root.mainloop()