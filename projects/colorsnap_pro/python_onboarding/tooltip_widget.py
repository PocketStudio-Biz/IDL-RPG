"""
ColorSnap Pro - Tooltip Widget (Python/PyQt6)
Contextual tooltips and hints for the application
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGraphicsDropShadowEffect, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont, QIcon
from typing import Optional, Callable

from onboarding_manager import TooltipType, TooltipContext, onboarding_manager


class TooltipWidget(QWidget):
    """
    A modern tooltip widget that can be shown anywhere in the app
    """
    dismissed = pyqtSignal()
    
    def __init__(self, tooltip: TooltipType, parent=None):
        super().__init__(parent)
        self.tooltip = tooltip
        self._auto_hide_timer: Optional[QTimer] = None
        
        self._setup_ui()
        self._apply_styling()
        self._add_shadow()
    
    def _setup_ui(self):
        """Setup the tooltip UI"""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Icon and title row
        header = QHBoxLayout()
        header.setSpacing(12)
        
        # Icon
        self.icon_label = QLabel(self.tooltip.icon)
        self.icon_label.setStyleSheet(f"font-size: 24px; color: {self._get_color()};")
        header.addWidget(self.icon_label)
        
        # Title
        self.title_label = QLabel(self.tooltip.title)
        self.title_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        header.addWidget(self.title_label)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Message
        self.message_label = QLabel(self.tooltip.message)
        self.message_label.setStyleSheet("""
            color: rgba(255, 255, 255, 200);
            font-size: 14px;
            line-height: 1.4;
        """)
        self.message_label.setWordWrap(True)
        self.message_label.setMinimumWidth(250)
        layout.addWidget(self.message_label)
        
        # Got it button
        self.got_it_btn = QPushButton("Got it!")
        self.got_it_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self._get_color()};
                color: white;
                border: none;
                border-radius: 16px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {self._get_hover_color()};
            }}
        """)
        self.got_it_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.got_it_btn.clicked.connect(self._on_dismiss)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.got_it_btn)
        layout.addLayout(btn_layout)
        
        self.setFixedWidth(320)
    
    def _apply_styling(self):
        """Apply glassmorphism styling"""
        color = self._get_color()
        self.setStyleSheet(f"""
            TooltipWidget {{
                background: rgba(30, 30, 40, 0.95);
                border: 2px solid {color}40;
                border-radius: 16px;
            }}
        """)
    
    def _add_shadow(self):
        """Add drop shadow effect"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)
    
    def _get_color(self) -> str:
        """Get color based on tooltip type"""
        colors = {
            TooltipType.CAMERA_PRESS_HOLD: "#3B82F6",
            TooltipType.CAMERA_FREEZE: "#3B82F6",
            TooltipType.CAMERA_AI: "#8B5CF6",
            TooltipType.CAMERA_COPY: "#3B82F6",
            TooltipType.PALETTE_SAVE: "#F97316",
            TooltipType.PALETTE_ORGANIZE: "#F97316",
            TooltipType.TOOLS_HARMONY: "#22C55E",
            TooltipType.TOOLS_CONTRAST: "#22C55E",
        }
        return colors.get(self.tooltip, "#3B82F6")
    
    def _get_hover_color(self) -> str:
        """Get hover color"""
        colors = {
            TooltipType.CAMERA_PRESS_HOLD: "#2563EB",
            TooltipType.CAMERA_FREEZE: "#2563EB",
            TooltipType.CAMERA_AI: "#7C3AED",
            TooltipType.CAMERA_COPY: "#2563EB",
            TooltipType.PALETTE_SAVE: "#EA580C",
            TooltipType.PALETTE_ORGANIZE: "#EA580C",
            TooltipType.TOOLS_HARMONY: "#16A34A",
            TooltipType.TOOLS_CONTRAST: "#16A34A",
        }
        return colors.get(self.tooltip, "#2563EB")
    
    def show_at(self, pos: QPoint, auto_hide_ms: int = 5000):
        """Show tooltip at specific position"""
        self.move(pos.x() - self.width() // 2, pos.y())
        self.show()
        
        # Animate in
        self.setWindowOpacity(0.0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(200)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()
        
        # Auto-hide
        if auto_hide_ms > 0:
            self._auto_hide_timer = QTimer(self)
            self._auto_hide_timer.singleShot(auto_hide_ms, self._on_dismiss)
    
    def _on_dismiss(self):
        """Handle dismiss"""
        # Mark as shown
        onboarding_manager.mark_tooltip_shown(self.tooltip)
        
        # Animate out
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(150)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self.anim.finished.connect(self.close)
        self.anim.start()
        
        self.dismissed.emit()


class InlineHint(QWidget):
    """
    Small inline hint widget for contextual tips
    """
    def __init__(self, text: str, icon: str = "💡", color: str = "#3B82F6", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            InlineHint {{
                background: {color}20;
                border: 1px solid {color}50;
                border-radius: 20px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 14px; color: {color};")
        layout.addWidget(icon_label)
        
        # Text
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            color: white;
            font-size: 13px;
            font-weight: 500;
        """)
        layout.addWidget(text_label)
    
    def show_with_animation(self):
        """Show with fade animation"""
        self.setWindowOpacity(0.0)
        self.show()
        
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()


class PulsingHintButton(QPushButton):
    """
    A pulsing hint button to draw attention
    """
    clicked_hint = pyqtSignal()
    
    def __init__(self, icon: str = "👆", parent=None):
        super().__init__(icon, parent)
        self.setFixedSize(50, 50)
        self.setStyleSheet("""
            QPushButton {
                background: rgba(253, 224, 71, 0.2);
                border: 2px solid #FDE047;
                border-radius: 25px;
                font-size: 20px;
            }
            QPushButton:hover {
                background: rgba(253, 224, 71, 0.3);
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Pulsing animation
        self._pulse_radius = 0
        self._pulse_opacity = 1.0
        self._pulse_timer = QTimer(self)
        self._pulse_timer.timeout.connect(self._update_pulse)
        self._pulse_timer.start(50)
        self._pulse_frame = 0
    
    def _update_pulse(self):
        """Update pulse animation"""
        self._pulse_frame += 1
        self.update()
    
    def paintEvent(self, event):
        """Custom paint with pulsing rings"""
        from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
        
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = self.rect().center()
        
        # Draw pulsing rings
        for i in range(2):
            phase = ((self._pulse_frame * 0.03) + i * 0.5) % 1.0
            radius = 25 + phase * 15
            opacity = 0.6 * (1 - phase)
            
            pen = QPen(QColor(253, 224, 71, int(opacity * 255)))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(QBrush())
            painter.drawEllipse(center, int(radius), int(radius))
        
        painter.end()


class TooltipManagerWidget(QWidget):
    """
    Manager widget that handles showing tooltips in context
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._active_tooltip: Optional[TooltipWidget] = None
    
    def show_tooltip(self, tooltip: TooltipType, position: Optional[QPoint] = None):
        """
        Show a tooltip if it hasn't been shown before
        
        Args:
            tooltip: The tooltip type to show
            position: Optional position, defaults to center of parent
        """
        # Check if already shown
        if onboarding_manager.has_shown_tooltip(tooltip):
            return
        
        # Hide any existing tooltip
        self.hide_current_tooltip()
        
        # Create and show new tooltip
        self._active_tooltip = TooltipWidget(tooltip, self.parent())
        
        if position is None:
            # Center in parent
            parent = self.parent()
            if parent:
                pos = parent.mapToGlobal(parent.rect().center())
                position = QPoint(pos.x(), pos.y() - 100)
            else:
                screen = QApplication.primaryScreen().geometry()
                position = QPoint(screen.center().x(), screen.center().y() - 100)
        
        self._active_tooltip.show_at(position)
        self._active_tooltip.dismissed.connect(self._on_tooltip_dismissed)
    
    def show_contextual_tooltip(self, context: TooltipContext, parent_widget=None):
        """Show the next tooltip for a given context"""
        tooltip = onboarding_manager.next_tooltip(context)
        if tooltip:
            self.show_tooltip(tooltip)
    
    def hide_current_tooltip(self):
        """Hide the currently shown tooltip"""
        if self._active_tooltip:
            self._active_tooltip.close()
            self._active_tooltip = None
    
    def _on_tooltip_dismissed(self):
        """Handle tooltip dismissal"""
        self._active_tooltip = None


class FirstTimeOverlay(QWidget):
    """
    Large overlay for first-time users with helpful hints
    """
    dismissed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        
        # Semi-transparent background
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background: rgba(0, 0, 0, 180);")
        
        # Hint card
        self.card = QFrame(self)
        self.card.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 40, 0.98);
                border: 2px solid rgba(253, 224, 71, 0.5);
                border-radius: 20px;
            }
        """)
        
        layout = QVBoxLayout(self.card)
        layout.setSpacing(16)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Icon
        icon = QLabel("👆")
        icon.setStyleSheet("font-size: 48px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)
        
        # Title
        title = QLabel("Press & Hold to Pick Colors")
        title.setStyleSheet("""
            color: white;
            font-size: 22px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Drag to adjust, release to capture")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 180);
            font-size: 15px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Feature hints
        hints_layout = QHBoxLayout()
        hints_layout.setSpacing(12)
        
        hint1 = InlineHint("Up to 5 colors", "🔢", "#22C55E")
        hint2 = InlineHint("Tap to copy hex", "📋", "#3B82F6")
        
        hints_layout.addStretch()
        hints_layout.addWidget(hint1)
        hints_layout.addWidget(hint2)
        hints_layout.addStretch()
        
        layout.addLayout(hints_layout)
        
        # Dismiss button
        dismiss_btn = QPushButton("Got it!")
        dismiss_btn.setStyleSheet("""
            QPushButton {
                background: #FDE047;
                color: #1a1a2e;
                border: none;
                border-radius: 12px;
                padding: 14px 32px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #FACC15;
            }
        """)
        dismiss_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        dismiss_btn.clicked.connect(self._on_dismiss)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(dismiss_btn)
        layout.addLayout(btn_layout)
        
        # Close when clicking overlay
        self.overlay.mousePressEvent = lambda e: self._on_dismiss()
        
        self.setVisible(False)
    
    def resizeEvent(self, event):
        """Handle resize"""
        super().resizeEvent(event)
        self.overlay.setGeometry(self.rect())
        
        # Center card
        card_size = self.card.sizeHint()
        x = (self.width() - card_size.width()) // 2
        y = (self.height() - card_size.height()) // 2
        self.card.move(x, y)
    
    def show_overlay(self):
        """Show the overlay with animation"""
        self.setVisible(True)
        self.overlay.setGeometry(self.rect())
        
        # Center card
        self.card.adjustSize()
        x = (self.width() - self.card.width()) // 2
        y = (self.height() - self.card.height()) // 2
        self.card.move(x, y)
        
        # Fade in
        self.setWindowOpacity(0.0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()
    
    def _on_dismiss(self):
        """Handle dismiss"""
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(200)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self._hide_complete)
        self.anim.start()
    
    def _hide_complete(self):
        """Complete hiding"""
        self.setVisible(False)
        self.dismissed.emit()


# Demo
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QMainWindow
    
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("Tooltip Demo")
    window.setMinimumSize(800, 600)
    window.setStyleSheet("background: #1a1a2e;")
    
    central = QWidget()
    window.setCentralWidget(central)
    
    layout = QVBoxLayout(central)
    
    # Tooltip manager
    tooltip_mgr = TooltipManagerWidget(central)
    
    # Buttons to show different tooltips
    def show_tooltip(t):
        pos = window.mapToGlobal(window.rect().center())
        tooltip_mgr.show_tooltip(t, QPoint(pos.x(), pos.y() - 50))
    
    from PyQt6.QtWidgets import QPushButton
    
    for tooltip_type in TooltipType:
        btn = QPushButton(f"Show: {tooltip_type.title}")
        btn.clicked.connect(lambda checked, t=tooltip_type: show_tooltip(t))
        layout.addWidget(btn)
    
    # First time overlay button
    overlay = None
    def show_overlay():
        global overlay
        overlay = FirstTimeOverlay(window)
        overlay.setGeometry(window.rect())
        overlay.show_overlay()
    
    overlay_btn = QPushButton("Show First Time Overlay")
    overlay_btn.clicked.connect(show_overlay)
    layout.addWidget(overlay_btn)
    
    window.show()
    sys.exit(app.exec())
