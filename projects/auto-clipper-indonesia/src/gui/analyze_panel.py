"""
Auto Clipper Indonesia - Analyze Panel
Video analysis and golden moment detection (REAL IMPLEMENTATION)
"""

import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
import sys

# Add core module path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

try:
    from video_analyzer import VideoAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False
    print("[WARNING] Video analyzer not available")


def create_analyze_panel(parent_frame, main_window):
    """Create the video analysis panel"""
    # Analysis info section
    info_frame = ctk.CTkFrame(parent_frame)
    info_frame.pack(fill="x", padx=20, pady=10)

    info_label = ctk.CTkLabel(
        info_frame,
        text="🎯 AI Analysis - Finding Golden Moments",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    info_label.pack(pady=10)

    # Status section
    status_frame = ctk.CTkFrame(parent_frame)
    status_frame.pack(fill="x", padx=20, pady=10)

    status_label = ctk.CTkLabel(
        status_frame,
        text="Status: Waiting for video...",
        font=ctk.CTkFont(size=14),
        text_color="gray"
    )
    status_label.pack(pady=10)

    # Progress bar
    progress_bar = ctk.CTkProgressBar(parent_frame)
    progress_bar.pack(fill="x", padx=20, pady=10)
    progress_bar.set(0)

    # Progress label
    progress_label = ctk.CTkLabel(
        parent_frame,
        text="",
        font=ctk.CTkFont(size=12)
    )
    progress_label.pack(pady=5)

    # Settings section
    settings_frame = ctk.CTkFrame(parent_frame)
    settings_frame.pack(fill="x", padx=20, pady=10)

    # Moments count
    moments_label = ctk.CTkLabel(
        settings_frame,
        text="Moments to detect:",
        font=ctk.CTkFont(size=14)
    )
    moments_label.pack(side="left", padx=10, pady=10)

    moments_var = ctk.StringVar(value="10")
    moments_entry = ctk.CTkEntry(
        settings_frame,
        width=80,
        textvariable=moments_var
    )
    moments_entry.pack(side="left", padx=5, pady=10)

    # Model size
    model_label = ctk.CTkLabel(
        settings_frame,
        text="Model:",
        font=ctk.CTkFont(size=14)
    )
    model_label.pack(side="left", padx=10, pady=10)

    model_var = ctk.StringVar(value="base")
    model_menu = ctk.CTkOptionMenu(
        settings_frame,
        values=["tiny", "base", "small", "medium"],
        variable=model_var
    )
    model_menu.pack(side="left", padx=5, pady=10)

    # Action buttons
    button_frame = ctk.CTkFrame(parent_frame)
    button_frame.pack(fill="x", padx=20, pady=10)

    start_button = ctk.CTkButton(
        button_frame,
        text="🚀 Start AI Analysis",
        height=40,
        width=200,
        fg_color="#2CC985",  # Green
        command=lambda: start_analysis(
            main_window, status_label, progress_bar, progress_label,
            int(moments_var.get()), model_var.get()
        )
    )
    start_button.pack(side="left", padx=5, pady=5)

    back_button = ctk.CTkButton(
        button_frame,
        text="← Back to Upload",
        height=40,
        width=160,
        command=lambda: main_window.tabview.set("Upload")
    )
    back_button.pack(side="left", padx=5, pady=5)

    return {
        'status_label': status_label,
        'progress_bar': progress_bar,
        'progress_label': progress_label,
        'moments_var': moments_var,
        'model_var': model_var
    }


def start_analysis(
    main_window, status_label, progress_bar, progress_label,
    moments_count: int, model_size: str
):
    """Start video analysis with real AI"""
    if not main_window.current_video_path:
        status_label.configure(
            text="❌ Error: No video loaded!",
            text_color="red"
        )
        messagebox.showerror("Error", "No video loaded! Please upload a video first.")
        return

    if not ANALYZER_AVAILABLE:
        status_label.configure(
            text="❌ AI Analyzer not installed",
            text_color="red"
        )
        messagebox.showerror("Error", "Video analyzer not available. Install dependencies:\n"
                                     "pip install faster-whisper textblob vaderSentiment")
        return

    # Disable button during analysis
    main_window.tabview.set("Analyze")
    status_label.configure(
        text="⏳ Loading AI models...",
        text_color="yellow"
    )
    progress_bar.set(0)
    main_window.update()

    try:
        # Initialize analyzer
        analyzer = VideoAnalyzer(model_size=model_size, device="cpu")

        def update_progress(progress):
            """Progress callback"""
            progress_bar.set(progress)
            if progress < 0.2:
                progress_label.configure(text="Loading AI models...")
            elif progress < 0.6:
                progress_label.configure(text="🎤 Transcribing audio...")
            elif progress < 0.8:
                progress_label.configure(text="🧠 Detecting golden moments...")
            elif progress < 0.95:
                progress_label.configure(text="✨ Analyzing content patterns...")
            else:
                progress_label.configure(text="✅ Finalizing results...")
            main_window.update()

        # Run analysis
        golden_moments = analyzer.find_golden_moments(
            main_window.current_video_path,
            progress_callback=update_progress
        )

        # Update UI
        progress_bar.set(1.0)
        status_label.configure(
            text=f"✅ Analysis Complete! Found {len(golden_moments)} golden moments",
            text_color="green"
        )
        progress_label.configure(text="Ready to select and export clips")

        # Store clips in main window
        main_window.analyzed_clips = golden_moments
        main_window.video_analyzer = analyzer

        print(f"[ANALYZE] ✅ Found {len(golden_moments)} golden moments")

        # Show summary
        if golden_moments:
            summary = analyzer.get_summary()
            clip_info = f"Type breakdown: {summary.get('types', {})}"
            print(f"[ANALYZE] {clip_info}")

            # Auto-switch to clip panel
            main_window.tabview.set("Clip")
        else:
            messagebox.showwarning("Warning", "No golden moments detected.\n"
                                              "Try with a longer video or different model.")

    except Exception as e:
        error_msg = str(e)
        status_label.configure(
            text=f"❌ Error: {error_msg[:50]}...",
            text_color="red"
        )
        progress_label.configure(text="Analysis failed")
        print(f"[ANALYZE] ❌ Error: {error_msg}")
        messagebox.showerror("Analysis Error", f"Failed to analyze video:\n{error_msg}")


if __name__ == "__main__":
    # Test analyze panel
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

    create_analyze_panel(test_frame, main_window)

    root.mainloop()