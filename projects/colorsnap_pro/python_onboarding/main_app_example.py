"""
ColorSnap Pro - Main Application Example (Python/PyQt6)
Example of how to integrate the onboarding system into a PyQt6 app
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QTabWidget, QFrame,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QColor, QPalette

from onboarding_manager import (
    OnboardingManager, 
    TooltipType, 
    TooltipContext,
    onboarding_manager
)
from onboarding_view import OnboardingWindow, TutorialWindow
from tooltip_widget import (
    TooltipManagerWidget, 
    FirstTimeOverlay,
    InlineHint,
    PulsingHintButton
)


class CameraTab(QWidget):
    """Example camera tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._check_first_time()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Camera preview placeholder
        self.preview = QFrame()
        self.preview.setFixedSize(640, 480)
        self.preview.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #ff6b6b, stop: 0.5 #feca57, stop: 1 #48dbfb);
                border-radius: 16px;
            }
        """)
        layout.addWidget(self.preview, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Hint label
        hint = InlineHint("Press & hold anywhere to pick colors", "👆", "#3B82F6")
        layout.addWidget(hint, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # First time overlay (initially hidden)
        self.first_time_overlay = FirstTimeOverlay(self.preview)
        
        # Tooltip manager
        self.tooltip_mgr = TooltipManagerWidget(self)
    
    def _check_first_time(self):
        """Check if we should show first-time hints"""
        if not onboarding_manager.has_picked_first_color:
            QTimer.singleShot(1000, self._show_first_time_overlay)
        
        # Show contextual tooltip
        QTimer.singleShot(2000, lambda: self.tooltip_mgr.show_contextual_tooltip(
            TooltipContext.CAMERA
        ))
    
    def _show_first_time_overlay(self):
        """Show first time overlay"""
        self.first_time_overlay.setGeometry(self.preview.rect())
        self.first_time_overlay.show_overlay()


class PaletteTab(QWidget):
    """Example palette tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel("🎨 Your Palettes")
        label.setStyleSheet("font-size: 24px; color: white;")
        layout.addWidget(label)
        
        # Tooltip manager
        self.tooltip_mgr = TooltipManagerWidget(self)
        
        # Show tooltip on appear
        QTimer.singleShot(500, lambda: self.tooltip_mgr.show_contextual_tooltip(
            TooltipContext.PALETTES
        ))


class ToolsTab(QWidget):
    """Example tools tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel("🛠️ Color Tools")
        label.setStyleSheet("font-size: 24px; color: white;")
        layout.addWidget(label)
        
        # Tooltip manager
        self.tooltip_mgr = TooltipManagerWidget(self)
        
        # Show tooltip on appear
        QTimer.singleShot(500, lambda: self.tooltip_mgr.show_contextual_tooltip(
            TooltipContext.TOOLS
        ))


class SettingsTab(QWidget):
    """Settings tab with onboarding controls"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        title = QLabel("⚙️ Settings")
        title.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
        layout.addWidget(title)
        
        # Onboarding status section
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding: 16px;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        
        status_title = QLabel("Onboarding Status")
        status_title.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        status_layout.addWidget(status_title)
        
        # Status items
        self.status_labels = {}
        statuses = [
            ("Onboarding Completed", "has_completed_onboarding"),
            ("Tutorial Seen", "has_seen_tutorial"),
            ("First Color Picked", "has_picked_first_color"),
            ("App Launches", "app_launch_count"),
        ]
        
        for label_text, key in statuses:
            row = QHBoxLayout()
            label = QLabel(label_text)
            label.setStyleSheet("color: rgba(255, 255, 255, 200); font-size: 14px;")
            row.addWidget(label)
            row.addStretch()
            
            value_label = QLabel("No")
            value_label.setStyleSheet("color: #EF4444; font-size: 14px; font-weight: bold;")
            row.addWidget(value_label)
            
            self.status_labels[key] = value_label
            status_layout.addLayout(row)
        
        layout.addWidget(status_frame)
        
        # Actions
        actions_title = QLabel("Actions")
        actions_title.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        layout.addWidget(actions_title)
        
        # Reset onboarding button
        reset_btn = QPushButton("🔄 Reset All Onboarding")
        reset_btn.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.2);
                color: #EF4444;
                border: 1px solid #EF4444;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.3);
            }
        """)
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.clicked.connect(self._reset_onboarding)
        layout.addWidget(reset_btn)
        
        # Show tutorial button
        tutorial_btn = QPushButton("📖 Show Tutorial Again")
        tutorial_btn.setStyleSheet("""
            QPushButton {
                background: rgba(59, 130, 246, 0.2);
                color: #3B82F6;
                border: 1px solid #3B82F6;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(59, 130, 246, 0.3);
            }
        """)
        tutorial_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        tutorial_btn.clicked.connect(self._show_tutorial)
        layout.addWidget(tutorial_btn)
        
        # Reset tooltips button
        tooltips_btn = QPushButton("💬 Reset Tooltips Only")
        tooltips_btn.setStyleSheet("""
            QPushButton {
                background: rgba(249, 115, 22, 0.2);
                color: #F97316;
                border: 1px solid #F97316;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(249, 115, 22, 0.3);
            }
        """)
        tooltips_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        tooltips_btn.clicked.connect(self._reset_tooltips)
        layout.addWidget(tooltips_btn)
        
        layout.addStretch()
        
        # Update status display
        self._update_status()
    
    def _update_status(self):
        """Update status labels"""
        status = onboarding_manager.get_all_status()
        
        for key, label in self.status_labels.items():
            value = status.get(key)
            if isinstance(value, bool):
                label.setText("Yes" if value else "No")
                label.setStyleSheet(
                    f"color: {'#22C55E' if value else '#EF4444'}; "
                    "font-size: 14px; font-weight: bold;"
                )
            else:
                label.setText(str(value))
                label.setStyleSheet("color: #3B82F6; font-size: 14px; font-weight: bold;")
    
    def _reset_onboarding(self):
        """Reset all onboarding state"""
        onboarding_manager.reset_all()
        self._update_status()
    
    def _show_tutorial(self):
        """Show tutorial window"""
        self.tutorial = TutorialWindow(self)
        self.tutorial.show()
    
    def _reset_tooltips(self):
        """Reset tooltip tracking"""
        onboarding_manager.reset_tooltips()
        self._update_status()
    
    def showEvent(self, event):
        """Update status when tab is shown"""
        super().showEvent(event)
        self._update_status()


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ColorSnap Pro")
        self.setMinimumSize(1000, 750)
        
        # Increment launch count
        onboarding_manager.increment_launch_count()
        
        self._setup_ui()
        self._apply_theme()
        self._check_onboarding()
    
    def _setup_ui(self):
        """Setup main UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)
        
        # Add tabs
        self.camera_tab = CameraTab()
        self.palette_tab = PaletteTab()
        self.tools_tab = ToolsTab()
        self.settings_tab = SettingsTab()
        
        self.tabs.addTab(self.camera_tab, "📷 Camera")
        self.tabs.addTab(self.palette_tab, "🎨 Palettes")
        self.tabs.addTab(self.tools_tab, "🛠️ Tools")
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")
        
        # Style tabs
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #0f0f1e;
            }
            QTabBar::tab {
                background: transparent;
                color: rgba(255, 255, 255, 150);
                padding: 12px 24px;
                font-size: 14px;
                border: none;
            }
            QTabBar::tab:selected {
                color: #3B82F6;
                border-top: 2px solid #3B82F6;
            }
            QTabBar::tab:hover:!selected {
                color: rgba(255, 255, 255, 200);
            }
        """)
        
        main_layout.addWidget(self.tabs)
    
    def _apply_theme(self):
        """Apply dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background: #0f0f1e;
            }
            QWidget {
                background: #0f0f1e;
            }
        """)
    
    def _check_onboarding(self):
        """Check if we should show onboarding"""
        if not onboarding_manager.has_completed_onboarding:
            # Show onboarding after short delay
            QTimer.singleShot(500, self._show_onboarding)
        elif not onboarding_manager.has_seen_tutorial:
            # Show tutorial if onboarding done but tutorial not seen
            QTimer.singleShot(500, self._show_tutorial)
    
    def _show_onboarding(self):
        """Show onboarding window"""
        self.onboarding = OnboardingWindow(self)
        self.onboarding.finished.connect(self._on_onboarding_finished)
        self.onboarding.skipped.connect(self._on_onboarding_finished)
        self.onboarding.show()
    
    def _on_onboarding_finished(self):
        """Handle onboarding completion"""
        onboarding_manager.complete_onboarding()
        # Show tutorial next
        self._show_tutorial()
    
    def _show_tutorial(self):
        """Show tutorial window"""
        self.tutorial = TutorialWindow(self)
        self.tutorial.finished.connect(
            lambda: onboarding_manager.complete_tutorial()
        )
        self.tutorial.show()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Dark theme
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#0f0f1e"))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor("#1a1a2e"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#16213e"))
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor("#1a1a2e"))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
