# 🎨 ColorSnap Pro - Onboarding System (Python/PyQt6)

A complete onboarding, tutorial, and tooltip system for Python desktop applications built with PyQt6.

## ✨ Features

- **5-Page Onboarding Walkthrough** - Beautiful animated slides with gradient backgrounds
- **Interactive Tutorial** - Step-by-step guide with progress indicators
- **Contextual Tooltips** - Smart tips based on user context (Camera, Palettes, Tools)
- **First-Time Hints** - Overlay hints for new users
- **Persistent State** - Tracks user progress using JSON storage
- **Debug Panel** - Settings to reset/view onboarding state

## 📁 Files

| File | Description |
|------|-------------|
| `onboarding_manager.py` | State management, persistence, and tracking |
| `onboarding_view.py` | OnboardingWindow and TutorialWindow classes |
| `tooltip_widget.py` | TooltipWidget, InlineHint, and overlay components |
| `main_app_example.py` | Complete example integration |
| `requirements.txt` | Python dependencies |

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Example

```bash
python main_app_example.py
```

## 📖 Usage

### Basic Onboarding

```python
from onboarding_manager import onboarding_manager
from onboarding_view import OnboardingWindow

# In your main window:
if not onboarding_manager.has_completed_onboarding:
    self.onboarding = OnboardingWindow(self)
    self.onboarding.finished.connect(onboarding_manager.complete_onboarding)
    self.onboarding.show()
```

### Tutorial

```python
from onboarding_view import TutorialWindow

# Show tutorial:
self.tutorial = TutorialWindow(self)
self.tutorial.finished.connect(onboarding_manager.complete_tutorial)
self.tutorial.show()
```

### Contextual Tooltips

```python
from tooltip_widget import TooltipManagerWidget
from onboarding_manager import TooltipContext

# In your widget:
self.tooltip_mgr = TooltipManagerWidget(self)

# Show next tooltip for camera context:
self.tooltip_mgr.show_contextual_tooltip(TooltipContext.CAMERA)
```

### First-Time Hints

```python
from tooltip_widget import FirstTimeOverlay

# Show overlay for first-time users:
if not onboarding_manager.has_picked_first_color:
    self.overlay = FirstTimeOverlay(self)
    self.overlay.show_overlay()
```

## 🎨 Customization

### Custom Onboarding Pages

```python
from onboarding_view import OnboardingWindow, OnboardingPage

window = OnboardingWindow()
window.pages = [
    OnboardingPage(
        icon="🚀",
        icon_color="#FF6B6B",
        title="Welcome",
        description="Your app description here",
        features=["Feature 1", "Feature 2", "Feature 3"]
    ),
    # Add more pages...
]
```

### Custom Tooltip Types

```python
from onboarding_manager import TooltipType

# Add new tooltip types to the enum:
class TooltipType(Enum):
    MY_CUSTOM_TIP = "my_custom_tip"
    
    @property
    def title(self) -> str:
        if self == TooltipType.MY_CUSTOM_TIP:
            return "My Custom Tip"
        # ...
    
    @property
    def message(self) -> str:
        if self == TooltipType.MY_CUSTOM_TIP:
            return "This is my custom tooltip message"
        # ...
```

## 🔧 API Reference

### OnboardingManager

```python
from onboarding_manager import onboarding_manager

# State
onboarding_manager.has_completed_onboarding  # bool
onboarding_manager.has_seen_tutorial         # bool
onboarding_manager.has_picked_first_color    # bool (get/set)
onboarding_manager.app_launch_count          # int

# Methods
onboarding_manager.complete_onboarding()
onboarding_manager.complete_tutorial()
onboarding_manager.increment_launch_count()
onboarding_manager.reset_all()
onboarding_manager.reset_tooltips()

# Tooltip management
onboarding_manager.has_shown_tooltip(TooltipType.CAMERA_PRESS_HOLD)
onboarding_manager.mark_tooltip_shown(TooltipType.CAMERA_PRESS_HOLD)
onboarding_manager.next_tooltip(TooltipContext.CAMERA)

# Debugging
onboarding_manager.get_all_status()  # Returns dict with all state
```

### OnboardingWindow

```python
from onboarding_view import OnboardingWindow

window = OnboardingWindow(parent)
window.finished.connect(callback)  # User completed all slides
window.skipped.connect(callback)   # User skipped onboarding
window.show()
```

### TutorialWindow

```python
from onboarding_view import TutorialWindow

window = TutorialWindow(parent)
window.finished.connect(callback)
window.show()
```

### TooltipManagerWidget

```python
from tooltip_widget import TooltipManagerWidget

manager = TooltipManagerWidget(parent)

# Show specific tooltip
manager.show_tooltip(TooltipType.CAMERA_PRESS_HOLD, position=QPoint(x, y))

# Show next contextual tooltip
manager.show_contextual_tooltip(TooltipContext.CAMERA)

# Hide current
manager.hide_current_tooltip()
```

### FirstTimeOverlay

```python
from tooltip_widget import FirstTimeOverlay

overlay = FirstTimeOverlay(parent_widget)
overlay.show_overlay()
overlay.dismissed.connect(callback)
```

### InlineHint

```python
from tooltip_widget import InlineHint

hint = InlineHint(
    text="Press & hold to pick colors",
    icon="👆",
    color="#3B82F6"
)
```

### PulsingHintButton

```python
from tooltip_widget import PulsingHintButton

btn = PulsingHintButton(icon="👆")
btn.clicked_hint.connect(callback)
```

## 💾 Data Storage

Onboarding state is stored in:
```
~/.colorsnap_pro/onboarding.json
```

Example content:
```json
{
  "has_completed_onboarding": true,
  "has_seen_tutorial": true,
  "has_picked_first_color": true,
  "app_launch_count": 5,
  "shown_tooltips": ["camera_press_hold", "camera_freeze"],
  "last_version": "1.0.0"
}
```

## 🎯 Tooltip Types

| Type | Title | When to Show |
|------|-------|--------------|
| `CAMERA_PRESS_HOLD` | Press & Hold | Camera tab, first visit |
| `CAMERA_FREEZE` | Freeze Frame | After picking first color |
| `CAMERA_AI` | AI Magic | Camera tab, after freeze shown |
| `CAMERA_COPY` | Quick Copy | After picking colors |
| `PALETTE_SAVE` | Save Colors | Palettes tab |
| `PALETTE_ORGANIZE` | Organize | Palettes tab |
| `TOOLS_HARMONY` | Color Harmony | Tools tab |
| `TOOLS_CONTRAST` | Check Contrast | Tools tab |

## 🔌 Integration Checklist

- [ ] Import `onboarding_manager` and call `increment_launch_count()` on app start
- [ ] Check `has_completed_onboarding` and show `OnboardingWindow` if False
- [ ] After onboarding, check `has_seen_tutorial` and show `TutorialWindow` if False
- [ ] Add `TooltipManagerWidget` to each main tab
- [ ] Show contextual tooltips using `show_contextual_tooltip()`
- [ ] Use `FirstTimeOverlay` for first-time user hints
- [ ] Add settings panel with onboarding reset options
- [ ] Call `mark_tooltip_shown()` when user performs relevant actions
- [ ] Set `has_picked_first_color = True` after first color selection

## 🎨 Theming

The default theme uses a dark gradient background. Customize by modifying stylesheets:

```python
# In your main window:
self.setStyleSheet("""
    QMainWindow {
        background: #your_color;
    }
""")
```

## 📄 License

MIT License - Free for personal and commercial use.
