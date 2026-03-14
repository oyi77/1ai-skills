"""
Auto Clipper Indonesia - Clip Panel
Select and configure clips to export
"""

import customtkinter as ctk


def create_clip_panel(parent_frame, main_window):
    """Create the clip selection and configuration panel"""

    # Header
    header_label = ctk.CTkLabel(
        parent_frame,
        text="Select Clips to Export",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    header_label.pack(pady=10)

    # Clips list frame
    clips_frame = ctk.CTkScrollableFrame(parent_frame, height=400)
    clips_frame.pack(fill="x", padx=20, pady=10)

    # Settings frame
    settings_frame = ctk.CTkFrame(parent_frame)
    settings_frame.pack(fill="x", padx=20, pady=10)

    # Duration setting
    duration_label = ctk.CTkLabel(
        settings_frame,
        text="Clip Duration:",
        font=ctk.CTkFont(size=14)
    )
    duration_label.pack(side="left", padx=10, pady=10)

    duration_slider = ctk.CTkSlider(
        settings_frame,
        from_=10,
        to=60,
        number_of_steps=10
    )
    duration_slider.set(30)
    duration_slider.pack(side="left", padx=10, pady=10)

    duration_value = ctk.CTkLabel(
        settings_frame,
        text="30s"
    )
    duration_value.pack(side="left", padx=5, pady=10)

    # Resolution setting
    resolution_label = ctk.CTkLabel(
        settings_frame,
        text="Resolution:",
        font=ctk.CTkFont(size=14)
    )
    resolution_label.pack(side="left", padx=10, pady=10)

    resolution_menu = ctk.CTkOptionMenu(
        settings_frame,
        values=["720p", "1080p"]
    )
    resolution_menu.set("720p")
    resolution_menu.pack(side="left", padx=10, pady=10)

    # Export button
    export_button = ctk.CTkButton(
        parent_frame,
        text="Export Clips",
        height=40,
        width=200,
        command=lambda: export_clips(main_window)
    )
    export_button.pack(pady=10)

    return clips_frame


def update_clips_list(clips_frame, clips):
    """Update the clips list with analyzed moments"""
    # Clear existing clips
    for widget in clips_frame.winfo_children():
        widget.destroy()

    if not clips:
        no_clips_label = ctk.CTkLabel(
            clips_frame,
            text="No clips detected. Analyze video first.",
            text_color="gray"
        )
        no_clips_label.pack(pady=20)
        return

    # Add each clip as a checkbox
    for i, clip in enumerate(clips):
        clip_frame = ctk.CTkFrame(clips_frame)
        clip_frame.pack(fill="x", padx=5, pady=5)

        # Checkbox
        checkbox = ctk.CTkCheckBox(
            clip_frame,
            text=f"Clip {i+1}: {clip['start']}s - {clip['end']}s"
        )
        checkbox.pack(side="left", padx=10, pady=5)

        # Score
        score_label = ctk.CTkLabel(
            clip_frame,
            text=f"Score: {clip['score']:.2f}",
            text_color="yellow"
        )
        score_label.pack(side="left", padx=10, pady=5)

        # Text preview
        text_label = ctk.CTkLabel(
            clip_frame,
            text=clip.get('text', ''[:50]),
            font=ctk.CTkFont(size=12)
        )
        text_label.pack(side="left", padx=10, pady=5)


def export_clips(main_window):
    """Export selected clips"""
    if not main_window.analyzed_clips:
        print("[EXPORT] No clips to export")
        return

    print(f"[EXPORT] Exporting {len(main_window.analyzed_clips)} clips...")
    # Export logic will be added
    main_window.tabview.set("Export")


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
    main_window.analyzed_clips = [
        {"start": 30, "end": 45, "score": 0.85, "text": "Test clip"},
    ]

    clips_frame = create_clip_panel(test_frame, main_window)
    update_clips_list(clips_frame, main_window.analyzed_clips)

    root.mainloop()