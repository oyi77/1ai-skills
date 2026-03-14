"""
Auto Clipper Indonesia - Upload Panel
Video upload functionality
"""

import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path


def create_upload_panel(parent_frame, main_window):
    """Create the video upload panel"""

    # Header
    header_label = ctk.CTkLabel(
        parent_frame,
        text="Upload Video",
        font=ctk.CTkFont(size=20, weight="bold")
    )
    header_label.pack(pady=20)

    # Upload area (drag and drop style)
    upload_frame = ctk.CTkFrame(parent_frame, height=300)
    upload_frame.pack(fill="x", padx=50, pady=10)

    # Upload instruction
    instruction_label = ctk.CTkLabel(
        upload_frame,
        text="Drop video here or click to browse",
        font=ctk.CTkFont(size=16)
    )
    instruction_label.pack(pady=20)

    # Upload button
    browse_button = ctk.CTkButton(
        upload_frame,
        text="Browse Video File",
        height=50,
        width=200,
        command=lambda: browse_video(parent_frame, main_window)
    )
    browse_button.pack(pady=10)

    # Selected file display
    selected_file_frame = ctk.CTkFrame(parent_frame)
    selected_file_frame.pack(fill="x", padx=50, pady=10)

    file_label = ctk.CTkLabel(
        selected_file_frame,
        text="No file selected",
        font=ctk.CTkFont(size=14),
        text_color="gray"
    )
    file_label.pack(pady=10)

    # Supported formats info
    formats_label = ctk.CTkLabel(
        parent_frame,
        text="Supported formats: MP4, AVI, MOV, MKV, WEBM",
        font=ctk.CTkFont(size=12),
        text_color="gray"
    )
    formats_label.pack(pady=10)

    # Analyze button (disabled initially)
    analyze_button = ctk.CTkButton(
        parent_frame,
        text="Analyze Video",
        height=40,
        width=200,
        state="disabled",
        command=lambda: analyze_video(main_window)
    )
    analyze_button.pack(pady=10)

    return {
        'file_label': file_label,
        'analyze_button': analyze_button
    }


def browse_video(parent_frame, main_window):
    """Open file dialog to select video"""
    file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[
            ('Video Files', '*.mp4 *.avi *.mov *.mkv *.webm'),
            ('All Files', '*.*')
        ]
    )

    if file_path:
        # Validate file
        path = Path(file_path)
        if path.exists() and path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            # Update UI
            main_window.set_video_path(str(path))

            # Get file info
            file_size = path.stat().st_size / (1024 * 1024)  # MB

            # Update file label
            upload_widgets = create_upload_panel(parent_frame, main_window)
            widget_container = parent_frame.winfo_children()
            for widget in widget_container:
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if isinstance(child, list) and len(child) > 0:
                            child[0].configure(
                                text=f"Selected: {path.name}",
                                text_color="white"
                            )
                            # Enable analyze button
                            if len(child) > 1:
                                child[1].configure(state="normal")

            print(f"[UPLOAD] Video selected: {path.name} ({file_size:.2f} MB)")
        else:
            print("[ERROR] Invalid video file")


def analyze_video(main_window):
    """Navigate to analyze tab"""
    main_window.tabview.set("Analyze")
    print("[UPLOAD] Moving to analyze tab...")


if __name__ == "__main__":
    # Test upload panel in isolation
    import sys
    import os

    # Add src to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    from gui.main_window import MainWindow

    import customtkinter as ctk

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1200x800")

    test_frame = ctk.CTkFrame(root)
    test_frame.pack(fill="both", expand=True)

    from gui.main_window import MainWindow
    main_window = MainWindow()

    create_upload_panel(test_frame, main_window)

    root.mainloop()