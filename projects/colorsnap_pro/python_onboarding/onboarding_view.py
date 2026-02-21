"""
ColorSnap Pro - Onboarding Views (Python/PyQt6)
Beautiful onboarding walkthrough with animated slides
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QGraphicsOpacityEffect,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer, 
    pyqtSignal, QParallelAnimationGroup, QPoint
)
from PyQt6.QtGui import (
    QFont, QFontDatabase, QColor, QPalette, 
    QLinearGradient, QBrush, QPainter, QIcon,
    QPixmap, QFontMetrics
)
from typing import List, Callable, Optional
import sys


class OnboardingPage:
    """Data class for onboarding page content"""
    def __init__(
        self,
        icon: str,
        icon_color: str,
        title: str,
        description: str,
        features: List[str]
    ):
        self.icon = icon
        self.icon_color = icon_color
        self.title = title
        self.description = description
        self.features = features


class AnimatedIcon(QFrame):
    """Animated icon with pulsing rings effect"""
    
    def __init__(self, icon_text: str, color: str, parent=None):
        super().__init__(parent)
        self.icon_text = icon_text
        self.color = QColor(color)
        self.setFixedSize(180, 180)
        self.setStyleSheet("background: transparent;")
        
        # Animation properties
        self._scale = 1.0
        self._opacity = 1.0
        self._ring_opacities = [0.6, 0.4, 0.2]
        self._ring_scales = [1.0, 1.15, 1.3]
        
        # Setup animations
        self._setup_animations()
    
    def _setup_animations(self):
        """Setup pulsing animations"""
        # Main pulse animation
        self.pulse_anim = QPropertyAnimation(self, b"minimumSize")
        self.pulse_anim.setDuration(2000)
        self.pulse_anim.setStartValue(self.size())
        self.pulse_anim.setEndValue(self.size() * 1.05)
        self.pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_anim.setLoopCount(-1)
        
        # Timer for continuous redraw
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_animation)
        self._timer.start(50)
        self._anim_frame = 0
    
    def _update_animation(self):
        """Update animation frame"""
        self._anim_frame += 1
        self.update()
    
    def paintEvent(self, event):
        """Custom paint for animated rings"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = self.rect().center()
        base_radius = 50
        
        # Animate rings
        for i, (base_opacity, base_scale) in enumerate(zip(self._ring_opacities, self._ring_scales)):
            # Calculate animated values
            phase = (self._anim_frame * 0.02 + i * 0.33) % 1.0
            scale = base_scale + phase * 0.2
            opacity = base_opacity * (1 - phase)
            
            # Draw ring
            painter.setPen(Qt.PenStyle.NoPen)
            color = QColor(self.color)
            color.setAlphaF(opacity)
            painter.setBrush(color)
            
            radius = int(base_radius * scale)
            painter.drawEllipse(center, radius, radius)
        
        # Draw main circle background
        painter.setBrush(self.color)
        painter.drawEllipse(center, base_radius, base_radius)
        
        # Draw inner highlight
        highlight = QColor(self.color)
        highlight.setAlphaF(0.3)
        painter.setBrush(highlight)
        painter.drawEllipse(center, int(base_radius * 0.85), int(base_radius * 0.85))
        
        painter.end()


class FeatureItem(QFrame):
    """Individual feature item with checkmark"""
    
    def __init__(self, text: str, color: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 4, 0, 4)
        
        # Checkmark icon
        check = QLabel("✓")
        check.setStyleSheet(f"""
            color: {color};
            font-size: 18px;
            font-weight: bold;
        """)
        layout.addWidget(check)
        
        # Feature text
        label = QLabel(text)
        label.setStyleSheet("""
            color: rgba(255, 255, 255, 230);
            font-size: 15px;
        """)
        layout.addWidget(label)
        layout.addStretch()


class OnboardingPageWidget(QWidget):
    """Individual onboarding page widget"""
    
    def __init__(self, page: OnboardingPage, parent=None):
        super().__init__(parent)
        self.page = page
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(24)
        layout.setContentsMargins(40, 20, 40, 20)
        
        # Animated icon
        self.icon = AnimatedIcon(self.page.icon, self.page.icon_color)
        layout.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel(self.page.title)
        title.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel(self.page.description)
        desc.setStyleSheet("""
            color: rgba(255, 255, 255, 200);
            font-size: 16px;
        """)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Features
        features_container = QWidget()
        features_layout = QVBoxLayout(features_container)
        features_layout.setSpacing(8)
        features_layout.setContentsMargins(20, 0, 20, 0)
        
        for feature in self.page.features:
            item = FeatureItem(feature, self.page.icon_color)
            features_layout.addWidget(item)
        
        layout.addWidget(features_container)
        layout.addStretch()


class OnboardingWindow(QMainWindow):
    """
    Main onboarding window with slide navigation
    """
    finished = pyqtSignal()
    skipped = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to ColorSnap Pro")
        self.setMinimumSize(900, 700)
        self.resize(900, 700)
        
        self.pages: List[OnboardingPage] = []
        self.current_page = 0
        
        self._setup_pages()
        self._setup_ui()
        self._apply_gradient_background()
    
    def _setup_pages(self):
        """Define onboarding pages"""
        self.pages = [
            OnboardingPage(
                icon="📷",
                icon_color="#3B82F6",
                title="Welcome to ColorSnap Pro",
                description="The ultimate color picking tool for designers, artists, and developers.",
                features=[
                    "Real-time camera color picking",
                    "Precision magnifier with crosshairs",
                    "Freeze frame for accuracy"
                ]
            ),
            OnboardingPage(
                icon="✨",
                icon_color="#8B5CF6",
                title="AI-Powered Palettes",
                description="Let AI analyze any scene and generate beautiful color palettes instantly.",
                features=[
                    "One-tap AI palette generation",
                    "Smart color extraction",
                    "Save palettes for later use"
                ]
            ),
            OnboardingPage(
                icon="🎨",
                icon_color="#F97316",
                title="Organize Your Colors",
                description="Keep all your colors organized in custom palettes for easy access.",
                features=[
                    "Create unlimited palettes",
                    "Copy hex codes with one tap",
                    "View RGB values instantly"
                ]
            ),
            OnboardingPage(
                icon="🛠️",
                icon_color="#22C55E",
                title="Professional Tools",
                description="Advanced tools to perfect your color choices.",
                features=[
                    "Color harmony generator",
                    "Contrast accessibility checker",
                    "Gradient maker with CSS export"
                ]
            ),
            OnboardingPage(
                icon="👆",
                icon_color="#EC4899",
                title="How to Pick Colors",
                description="It's simple! Just point, press, and capture.",
                features=[
                    "Press & hold to preview colors",
                    "Drag to fine-tune selection",
                    "Release to capture up to 5 colors",
                    "Tap colors to copy hex codes"
                ]
            )
        ]
    
    def _setup_ui(self):
        """Setup the main UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Skip button at top
        skip_layout = QHBoxLayout()
        skip_layout.addStretch()
        
        self.skip_btn = QPushButton("Skip")
        self.skip_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: rgba(255, 255, 255, 180);
                border: none;
                padding: 12px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        self.skip_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.skip_btn.clicked.connect(self._on_skip)
        skip_layout.addWidget(self.skip_btn)
        
        main_layout.addLayout(skip_layout)
        
        # Stacked widget for pages
        self.stack = QStackedWidget()
        for page_data in self.pages:
            page_widget = OnboardingPageWidget(page_data)
            self.stack.addWidget(page_widget)
        
        main_layout.addWidget(self.stack, 1)
        
        # Page indicators
        indicators_layout = QHBoxLayout()
        indicators_layout.setSpacing(8)
        indicators_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.indicators: List[QFrame] = []
        for i in range(len(self.pages)):
            indicator = QFrame()
            indicator.setFixedSize(8 if i != 0 else 24, 8)
            indicator.setStyleSheet(f"""
                QFrame {{
                    background: {'white' if i == 0 else 'rgba(255, 255, 255, 0.3)'};
                    border-radius: 4px;
                }}
            """)
            indicators_layout.addWidget(indicator)
            self.indicators.append(indicator)
        
        main_layout.addLayout(indicators_layout)
        main_layout.addSpacing(24)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(16)
        nav_layout.setContentsMargins(24, 0, 24, 24)
        
        # Back button
        self.back_btn = QPushButton("←")
        self.back_btn.setFixedSize(56, 56)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.15);
                color: white;
                border: none;
                border-radius: 28px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.25);
            }
            QPushButton:disabled {
                background: transparent;
                color: transparent;
            }
        """)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.clicked.connect(self._on_back)
        self.back_btn.setEnabled(False)
        nav_layout.addWidget(self.back_btn)
        
        nav_layout.addStretch()
        
        # Next/Start button
        self.next_btn = QPushButton("Next →")
        self.next_btn.setFixedHeight(56)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #3B82F6, stop: 1 #8B5CF6);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 32px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #2563EB, stop: 1 #7C3AED);
            }
        """)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.clicked.connect(self._on_next)
        nav_layout.addWidget(self.next_btn)
        
        main_layout.addLayout(nav_layout)
    
    def _apply_gradient_background(self):
        """Apply gradient background to window"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1a1a2e, stop: 0.5 #16213e, stop: 1 #0f3460);
            }
        """)
    
    def _update_indicators(self):
        """Update page indicator styles"""
        for i, indicator in enumerate(self.indicators):
            is_active = i == self.current_page
            indicator.setFixedSize(24 if is_active else 8, 8)
            indicator.setStyleSheet(f"""
                QFrame {{
                    background: {'white' if is_active else 'rgba(255, 255, 255, 0.3)'};
                    border-radius: 4px;
                }}
            """)
    
    def _on_next(self):
        """Handle next button click"""
        if self.current_page < len(self.pages) - 1:
            # Animate transition
            self._animate_page_transition(self.current_page + 1)
        else:
            # Finished
            self.finished.emit()
            self.close()
    
    def _on_back(self):
        """Handle back button click"""
        if self.current_page > 0:
            self._animate_page_transition(self.current_page - 1)
    
    def _on_skip(self):
        """Handle skip button click"""
        self.skipped.emit()
        self.close()
    
    def _animate_page_transition(self, new_page: int):
        """Animate transition between pages"""
        # Fade out current
        current_widget = self.stack.widget(self.current_page)
        effect = QGraphicsOpacityEffect(current_widget)
        current_widget.setGraphicsEffect(effect)
        
        fade_out = QPropertyAnimation(effect, b"opacity")
        fade_out.setDuration(150)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        
        def on_fade_out_finished():
            self.current_page = new_page
            self.stack.setCurrentIndex(new_page)
            self._update_indicators()
            self._update_buttons()
            
            # Fade in new
            new_widget = self.stack.widget(self.current_page)
            new_effect = QGraphicsOpacityEffect(new_widget)
            new_widget.setGraphicsEffect(new_effect)
            
            fade_in = QPropertyAnimation(new_effect, b"opacity")
            fade_in.setDuration(200)
            fade_in.setStartValue(0.0)
            fade_in.setEndValue(1.0)
            fade_in.start()
        
        fade_out.finished.connect(on_fade_out_finished)
        fade_out.start()
    
    def _update_buttons(self):
        """Update button states"""
        self.back_btn.setEnabled(self.current_page > 0)
        
        if self.current_page == len(self.pages) - 1:
            self.next_btn.setText("Get Started ✓")
        else:
            self.next_btn.setText("Next →")


class TutorialStep:
    """Data class for tutorial step"""
    def __init__(
        self,
        title: str,
        description: str,
        icon: str,
        color: str = "#3B82F6"
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.color = color


class TutorialWindow(QMainWindow):
    """
    Interactive tutorial window with step-by-step guide
    """
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tutorial")
        self.setMinimumSize(600, 500)
        self.resize(600, 500)
        
        self.steps = [
            TutorialStep(
                title="Press & Hold",
                description="Press and hold anywhere on the camera preview to preview colors",
                icon="👆",
                color="#3B82F6"
            ),
            TutorialStep(
                title="Magnifier",
                description="The magnifier appears above your cursor with precise crosshairs",
                icon="🔍",
                color="#8B5CF6"
            ),
            TutorialStep(
                title="Drag to Adjust",
                description="Drag to fine-tune the exact color you want",
                icon="↔️",
                color="#3B82F6"
            ),
            TutorialStep(
                title="Release to Capture",
                description="Release to save the color. You can capture up to 5 colors!",
                icon="✓",
                color="#22C55E"
            ),
            TutorialStep(
                title="Freeze Frame",
                description="Tap Freeze Frame to pause the camera for easier picking",
                icon="❄️",
                color="#22C55E"
            )
        ]
        
        self.current_step = 0
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self):
        """Setup tutorial UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(24)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Progress bar
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(8)
        self.progress_bars = []
        
        for i in range(len(self.steps)):
            bar = QFrame()
            bar.setFixedSize(80, 4)
            bar.setStyleSheet(f"""
                background: {'#3B82F6' if i == 0 else 'rgba(255, 255, 255, 0.3)'};
                border-radius: 2px;
            """)
            progress_layout.addWidget(bar)
            self.progress_bars.append(bar)
        
        layout.addLayout(progress_layout)
        layout.addSpacing(20)
        
        # Icon
        self.icon_label = QLabel(self.steps[0].icon)
        self.icon_label.setStyleSheet("font-size: 64px;")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_label)
        
        # Title
        self.title_label = QLabel(self.steps[0].title)
        self.title_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Description
        self.desc_label = QLabel(self.steps[0].description)
        self.desc_label.setStyleSheet("""
            color: rgba(255, 255, 255, 200);
            font-size: 16px;
        """)
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        layout.addStretch()
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("Back")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: rgba(255, 255, 255, 180);
                border: none;
                padding: 12px 24px;
                font-size: 14px;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.clicked.connect(self._on_back)
        self.back_btn.setVisible(False)
        nav_layout.addWidget(self.back_btn)
        
        nav_layout.addStretch()
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 32px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2563EB;
            }
        """)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.clicked.connect(self._on_next)
        nav_layout.addWidget(self.next_btn)
        
        layout.addLayout(nav_layout)
    
    def _apply_styles(self):
        """Apply window styles"""
        self.setStyleSheet("""
            QMainWindow {
                background: #0f0f1e;
            }
        """)
    
    def _update_ui(self):
        """Update UI for current step"""
        step = self.steps[self.current_step]
        
        self.icon_label.setText(step.icon)
        self.title_label.setText(step.title)
        self.desc_label.setText(step.description)
        
        # Update progress bars
        for i, bar in enumerate(self.progress_bars):
            color = step.color if i <= self.current_step else "rgba(255, 255, 255, 0.3)"
            bar.setStyleSheet(f"background: {color}; border-radius: 2px;")
        
        # Update buttons
        self.back_btn.setVisible(self.current_step > 0)
        
        if self.current_step == len(self.steps) - 1:
            self.next_btn.setText("Start Picking!")
        else:
            self.next_btn.setText("Next")
    
    def _on_next(self):
        """Handle next button"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._update_ui()
        else:
            self.finished.emit()
            self.close()
    
    def _on_back(self):
        """Handle back button"""
        if self.current_step > 0:
            self.current_step -= 1
            self._update_ui()


def show_onboarding(parent=None) -> OnboardingWindow:
    """Convenience function to show onboarding window"""
    window = OnboardingWindow(parent)
    window.show()
    return window


def show_tutorial(parent=None) -> TutorialWindow:
    """Convenience function to show tutorial window"""
    window = TutorialWindow(parent)
    window.show()
    return window


# Demo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Dark theme
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#0f0f1e"))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = show_onboarding()
    window.finished.connect(lambda: print("Onboarding completed!"))
    window.skipped.connect(lambda: print("Onboarding skipped!"))
    
    sys.exit(app.exec())
