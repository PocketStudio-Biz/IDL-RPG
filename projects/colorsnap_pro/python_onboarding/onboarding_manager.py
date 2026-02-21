"""
ColorSnap Pro - Onboarding Manager (Python/PyQt6)
Manages onboarding state and tracks which tips/tooltips have been shown
"""

import json
import os
from enum import Enum
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, asdict, field


class TooltipType(Enum):
    """Types of tooltips that can be shown"""
    CAMERA_PRESS_HOLD = "camera_press_hold"
    CAMERA_FREEZE = "camera_freeze"
    CAMERA_AI = "camera_ai"
    CAMERA_COPY = "camera_copy"
    PALETTE_SAVE = "palette_save"
    PALETTE_ORGANIZE = "palette_organize"
    TOOLS_HARMONY = "tools_harmony"
    TOOLS_CONTRAST = "tools_contrast"
    
    @property
    def title(self) -> str:
        titles = {
            TooltipType.CAMERA_PRESS_HOLD: "Press & Hold",
            TooltipType.CAMERA_FREEZE: "Freeze Frame",
            TooltipType.CAMERA_AI: "AI Magic",
            TooltipType.CAMERA_COPY: "Quick Copy",
            TooltipType.PALETTE_SAVE: "Save Colors",
            TooltipType.PALETTE_ORGANIZE: "Organize",
            TooltipType.TOOLS_HARMONY: "Color Harmony",
            TooltipType.TOOLS_CONTRAST: "Check Contrast",
        }
        return titles.get(self, "Tip")
    
    @property
    def message(self) -> str:
        messages = {
            TooltipType.CAMERA_PRESS_HOLD: "Press and hold anywhere to preview colors with the magnifier",
            TooltipType.CAMERA_FREEZE: "Tap Freeze Frame to pause the camera for precise picking",
            TooltipType.CAMERA_AI: "Try AI Palette to automatically generate color schemes",
            TooltipType.CAMERA_COPY: "Tap any picked color to copy its hex code",
            TooltipType.PALETTE_SAVE: "Save your captured colors to a palette for later",
            TooltipType.PALETTE_ORGANIZE: "Create multiple palettes to organize your projects",
            TooltipType.TOOLS_HARMONY: "Generate complementary, analogous, and triadic colors",
            TooltipType.TOOLS_CONTRAST: "Ensure your colors meet accessibility standards",
        }
        return messages.get(self, "")
    
    @property
    def icon(self) -> str:
        icons = {
            TooltipType.CAMERA_PRESS_HOLD: "hand.tap.fill",
            TooltipType.CAMERA_FREEZE: "snowflake",
            TooltipType.CAMERA_AI: "wand.and.stars",
            TooltipType.CAMERA_COPY: "doc.on.doc",
            TooltipType.PALETTE_SAVE: "folder.badge.plus",
            TooltipType.PALETTE_ORGANIZE: "swatchpalette",
            TooltipType.TOOLS_HARMONY: "circle.hexagongrid",
            TooltipType.TOOLS_CONTRAST: "textformat.size",
        }
        return icons.get(self, "info.circle")


class TooltipContext(Enum):
    """Context for showing tooltips"""
    CAMERA = "camera"
    PALETTES = "palettes"
    TOOLS = "tools"


@dataclass
class OnboardingState:
    """Data class for onboarding state"""
    has_completed_onboarding: bool = False
    has_seen_tutorial: bool = False
    has_picked_first_color: bool = False
    app_launch_count: int = 0
    shown_tooltips: List[str] = field(default_factory=list)
    last_version: Optional[str] = None


class OnboardingManager:
    """
    Singleton manager for onboarding state and preferences.
    Uses JSON file for persistence.
    """
    _instance: Optional['OnboardingManager'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if OnboardingManager._initialized:
            return
            
        self._config_dir = os.path.join(os.path.expanduser("~"), ".colorsnap_pro")
        self._config_file = os.path.join(self._config_dir, "onboarding.json")
        self._state = OnboardingState()
        
        self._ensure_config_dir()
        self._load_state()
        
        OnboardingManager._initialized = True
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        if not os.path.exists(self._config_dir):
            os.makedirs(self._config_dir)
    
    def _load_state(self):
        """Load state from JSON file"""
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r') as f:
                    data = json.load(f)
                    self._state = OnboardingState(**data)
            except (json.JSONDecodeError, TypeError):
                self._state = OnboardingState()
    
    def _save_state(self):
        """Save state to JSON file"""
        with open(self._config_file, 'w') as f:
            json.dump(asdict(self._state), f, indent=2)
    
    # MARK: - Onboarding State
    
    @property
    def has_completed_onboarding(self) -> bool:
        return self._state.has_completed_onboarding
    
    def complete_onboarding(self):
        """Mark onboarding as completed"""
        self._state.has_completed_onboarding = True
        self._save_state()
    
    def reset_onboarding(self):
        """Reset onboarding state"""
        self._state.has_completed_onboarding = False
        self._state.has_seen_tutorial = False
        self._state.app_launch_count = 0
        self._state.shown_tooltips = []
        self._save_state()
    
    # MARK: - Tutorial State
    
    @property
    def has_seen_tutorial(self) -> bool:
        return self._state.has_seen_tutorial
    
    def complete_tutorial(self):
        """Mark tutorial as seen"""
        self._state.has_seen_tutorial = True
        self._save_state()
    
    # MARK: - Tooltip Tracking
    
    def has_shown_tooltip(self, tooltip: TooltipType) -> bool:
        """Check if a tooltip has been shown"""
        return tooltip.value in self._state.shown_tooltips
    
    def mark_tooltip_shown(self, tooltip: TooltipType):
        """Mark a tooltip as shown"""
        if tooltip.value not in self._state.shown_tooltips:
            self._state.shown_tooltips.append(tooltip.value)
            self._save_state()
    
    def reset_tooltips(self):
        """Reset all tooltip tracking"""
        self._state.shown_tooltips = []
        self._save_state()
    
    # MARK: - First Color Pick
    
    @property
    def has_picked_first_color(self) -> bool:
        return self._state.has_picked_first_color
    
    @has_picked_first_color.setter
    def has_picked_first_color(self, value: bool):
        self._state.has_picked_first_color = value
        self._save_state()
    
    # MARK: - App Launch Count
    
    @property
    def app_launch_count(self) -> int:
        return self._state.app_launch_count
    
    def increment_launch_count(self):
        """Increment the app launch counter"""
        self._state.app_launch_count += 1
        self._save_state()
    
    # MARK: - Version Tracking
    
    @property
    def last_version(self) -> Optional[str]:
        return self._state.last_version
    
    def set_current_version(self, version: str):
        """Set the current app version"""
        self._state.last_version = version
        self._save_state()
    
    def is_new_version(self, version: str) -> bool:
        """Check if this is a new version"""
        return self._state.last_version != version
    
    # MARK: - Contextual Tips
    
    def next_tooltip(self, context: TooltipContext) -> Optional[TooltipType]:
        """Get the next tooltip to show for a given context"""
        if context == TooltipContext.CAMERA:
            priority = [
                TooltipType.CAMERA_PRESS_HOLD,
                TooltipType.CAMERA_FREEZE,
                TooltipType.CAMERA_AI,
                TooltipType.CAMERA_COPY,
            ]
        elif context == TooltipContext.PALETTES:
            priority = [
                TooltipType.PALETTE_SAVE,
                TooltipType.PALETTE_ORGANIZE,
            ]
        elif context == TooltipContext.TOOLS:
            priority = [
                TooltipType.TOOLS_HARMONY,
                TooltipType.TOOLS_CONTRAST,
            ]
        else:
            return None
        
        for tooltip in priority:
            if not self.has_shown_tooltip(tooltip):
                return tooltip
        return None
    
    # MARK: - Complete Reset
    
    def reset_all(self):
        """Reset all onboarding state"""
        self.reset_onboarding()
        self._state.has_picked_first_color = False
        self._save_state()
    
    def get_all_status(self) -> Dict[str, Any]:
        """Get full status for debugging"""
        return {
            "has_completed_onboarding": self.has_completed_onboarding,
            "has_seen_tutorial": self.has_seen_tutorial,
            "has_picked_first_color": self.has_picked_first_color,
            "app_launch_count": self.app_launch_count,
            "shown_tooltips": self._state.shown_tooltips,
            "last_version": self.last_version,
        }


# Global singleton instance
onboarding_manager = OnboardingManager()
