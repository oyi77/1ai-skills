"""
Auto Clipper Indonesia - Main Window
Primary GUI application window
"""

import customtkinter as ctk
from pathlib import Path


class MainWindow(ctk.CTk):
    """Main application window for Auto Clipper Indonesia"""

    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Auto Clipper Indonesia")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # State
        self.current_video_path = None
        self.analyzed_clips = []
        self.selected_clips = []

        # Build UI
        self._setup_ui()

    def _setup_ui(self):
        """Build the main user interface"""

        # Create main frame with padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(main_frame, height=60)
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = ctk.CTkLabel(
            header_frame,
            text="Auto Clipper Indonesia",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=10)

        version_label = ctk.CTkLabel(
            header_frame,
            text="v1.0.0-MVP",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        version_label.pack(side="right", padx=20, pady=10)

        # Content area (will be filled with panels)
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Navigation tabs
        self.tabview = ctk.CTkTabview(self.content_frame)
        self.tabview.pack(fill="both", expand=True)

        # Create tabs
        self.upload_tab = self.tabview.add("Upload")
        self.analyze_tab = self.tabview.add("Analyze")
        self.clip_tab = self.tabview.add("Clip")
        self.export_tab = self.tabview.add("Export")

        # Initialize each tab
        self._init_upload_tab()
        self._init_analyze_tab()
        self._init_clip_tab()
        self._init_export_tab()

    def _init_upload_tab(self):
        """Initialize upload tab"""
        import gui.upload_panel as upload_panel
        upload_panel.create_upload_panel(self.upload_tab, self)

    def _init_analyze_tab(self):
        """Initialize analyze tab"""
        import gui.analyze_panel as analyze_panel
        analyze_panel.create_analyze_panel(self.analyze_tab, self)

    def _init_clip_tab(self):
        """Initialize clip tab"""
        import gui.clip_panel as clip_panel
        clip_panel.create_clip_panel(self.clip_tab, self)

    def _init_export_tab(self):
        """Initialize export tab"""
        import gui.export_panel as export_panel
        export_panel.create_export_panel(self.export_tab, self)

    def set_video_path(self, path: str):
        """Set the current video file path"""
        self.current_video_path = path
        self.log_info(f"Video loaded: {path}")

    def log_info(self, message: str):
        """Log info message to console"""
        print(f"[INFO] {message}")


if __name__ == "__main__":
    # Test main window
    app = MainWindow()
    app.mainloop()