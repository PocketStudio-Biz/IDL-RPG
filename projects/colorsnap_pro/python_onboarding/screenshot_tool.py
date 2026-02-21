"""
ColorSnap Pro - Screenshot Tool for Python Desktop App
Captures screenshots for documentation and marketing
"""

import sys
import os
from datetime import datetime
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QFileDialog, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, QDir
from PyQt6.QtGui import QPixmap, QScreen, QColor, QPalette


class ScreenshotTool(QMainWindow):
    """Tool for capturing app screenshots"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ColorSnap Pro Screenshot Tool")
        self.setMinimumSize(400, 200)
        
        self.output_dir = os.path.expanduser("~/colorsnap_screenshots")
        self._setup_ui()
        self._apply_theme()
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _setup_ui(self):
        """Setup UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("📸 Screenshot Tool")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Output directory
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel(f"Output: {self.output_dir}")
        self.dir_label.setStyleSheet("color: rgba(255,255,255,180);")
        dir_layout.addWidget(self.dir_label)
        
        change_btn = QPushButton("Change")
        change_btn.setStyleSheet("""
            QPushButton {
                background: #3B82F6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover { background: #2563EB; }
        """)
        change_btn.clicked.connect(self._change_output_dir)
        dir_layout.addWidget(change_btn)
        layout.addLayout(dir_layout)
        
        # Screenshots list
        screenshots = [
            ("Camera Picker", "main_camera_view"),
            ("Frozen Frame", "frozen_frame_view"),
            ("Palette List", "palette_list"),
            ("Palette Detail", "palette_detail"),
            ("Color Harmony Tool", "color_harmony"),
            ("Contrast Checker", "contrast_checker"),
            ("Gradient Maker", "gradient_maker"),
            ("Settings", "settings"),
            ("Onboarding 1", "onboarding_01"),
            ("Onboarding 2", "onboarding_02"),
            ("Onboarding 3", "onboarding_03"),
        ]
        
        self.screenshot_buttons = []
        for name, filename in screenshots:
            btn = QPushButton(f"📷 Capture: {name}")
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255,255,255,0.1);
                    color: white;
                    border: 1px solid rgba(255,255,255,0.2);
                    border-radius: 8px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background: rgba(255,255,255,0.15);
                    border-color: #3B82F6;
                }
            """)
            btn.clicked.connect(lambda checked, n=name, f=filename: self._capture_screenshot(n, f))
            layout.addWidget(btn)
            self.screenshot_buttons.append((btn, name, filename))
        
        # Capture all button
        layout.addSpacing(10)
        self.capture_all_btn = QPushButton("📸 Capture All Screenshots")
        self.capture_all_btn.setStyleSheet("""
            QPushButton {
                background: #22C55E;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background: #16A34A; }
            QPushButton:disabled { background: #666; }
        """)
        self.capture_all_btn.clicked.connect(self._capture_all)
        layout.addWidget(self.capture_all_btn)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background: rgba(255,255,255,0.1);
            }
            QProgressBar::chunk {
                background: #3B82F6;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: rgba(255,255,255,150);")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Open folder button
        open_btn = QPushButton("📁 Open Screenshots Folder")
        open_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #3B82F6;
                border: 1px solid #3B82F6;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: rgba(59,130,246,0.1);
            }
        """)
        open_btn.clicked.connect(self._open_folder)
        layout.addWidget(open_btn)
    
    def _apply_theme(self):
        """Apply dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background: #0f0f1e;
            }
        """)
    
    def _change_output_dir(self):
        """Change output directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory", self.output_dir)
        if dir_path:
            self.output_dir = dir_path
            self.dir_label.setText(f"Output: {self.output_dir}")
            os.makedirs(self.output_dir, exist_ok=True)
    
    def _capture_screenshot(self, name: str, filename: str):
        """Capture a single screenshot"""
        self.status_label.setText(f"Capturing {name}...")
        
        # Hide this window
        self.hide()
        QTimer.singleShot(500, lambda: self._do_capture(name, filename))
    
    def _do_capture(self, name: str, filename: str):
        """Actually capture the screenshot"""
        # Get primary screen
        screen = QApplication.primaryScreen()
        if not screen:
            self.show()
            self.status_label.setText("❌ Failed: No screen found")
            return
        
        # Capture
        screenshot = screen.grabWindow(0)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"{filename}_{timestamp}.png")
        screenshot.save(filepath, "PNG")
        
        # Show this window again
        self.show()
        self.status_label.setText(f"✅ Saved: {filepath}")
    
    def _capture_all(self):
        """Capture all screenshots in sequence"""
        self.capture_all_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setMaximum(len(self.screenshot_buttons))
        self.progress.setValue(0)
        
        self._capture_index = 0
        self._capture_next()
    
    def _capture_next(self):
        """Capture next screenshot in sequence"""
        if self._capture_index >= len(self.screenshot_buttons):
            # Done
            self.capture_all_btn.setEnabled(True)
            self.progress.setVisible(False)
            self.status_label.setText(f"✅ All {len(self.screenshot_buttons)} screenshots saved!")
            self.show()
            return
        
        btn, name, filename = self.screenshot_buttons[self._capture_index]
        self.progress.setValue(self._capture_index)
        self.status_label.setText(f"Capturing {name} ({self._capture_index + 1}/{len(self.screenshot_buttons)})...")
        
        # Hide window
        self.hide()
        
        # Capture after delay
        QTimer.singleShot(1000, lambda: self._do_capture_and_continue(name, filename))
    
    def _do_capture_and_continue(self, name: str, filename: str):
        """Capture and continue to next"""
        screen = QApplication.primaryScreen()
        if screen:
            screenshot = screen.grabWindow(0)
            filepath = os.path.join(self.output_dir, f"{filename}.png")
            screenshot.save(filepath, "PNG")
        
        self._capture_index += 1
        self._capture_next()
    
    def _open_folder(self):
        """Open screenshots folder"""
        import subprocess
        
        if sys.platform == "darwin":
            subprocess.run(["open", self.output_dir])
        elif sys.platform == "win32":
            subprocess.run(["explorer", self.output_dir])
        else:
            subprocess.run(["xdg-open", self.output_dir])


def capture_app_screenshots(app_window: QMainWindow, output_dir: Optional[str] = None):
    """
    Programmatically capture screenshots of an app window
    
    Usage:
        from screenshot_tool import capture_app_screenshots
        capture_app_screenshots(main_window, "~/screenshots")
    """
    if output_dir is None:
        output_dir = os.path.expanduser("~/colorsnap_screenshots")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Ensure window is visible and rendered
    app_window.show()
    app_window.raise_()
    app_window.activateWindow()
    QApplication.processEvents()
    
    # Wait for rendering
    QTimer.singleShot(500, lambda: _do_capture_window(app_window, output_dir))


def _do_capture_window(window: QMainWindow, output_dir: str):
    """Capture window screenshot"""
    # Capture the window
    screenshot = window.grab()
    
    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    window_title = window.windowTitle().replace(" ", "_").lower()
    filepath = os.path.join(output_dir, f"{window_title}_{timestamp}.png")
    
    screenshot.save(filepath, "PNG")
    print(f"Screenshot saved: {filepath}")


# Standalone screenshot tool entry point
def main():
    app = QApplication(sys.argv)
    
    # Dark theme
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#0f0f1e"))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = ScreenshotTool()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
