"""
Test script for the onboarding system (no GUI required)
Run this to verify the onboarding logic works correctly.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from onboarding_manager import (
    OnboardingManager, 
    TooltipType, 
    TooltipContext,
    onboarding_manager
)


def test_singleton():
    """Test that OnboardingManager is a singleton"""
    print("\n🧪 Testing Singleton Pattern...")
    manager1 = OnboardingManager()
    manager2 = OnboardingManager()
    assert manager1 is manager2, "OnboardingManager should be singleton"
    print("   ✅ Singleton pattern works correctly")


def test_initial_state():
    """Test initial state of onboarding manager"""
    print("\n🧪 Testing Initial State...")
    
    # Reset for clean test
    onboarding_manager.reset_all()
    
    assert not onboarding_manager.has_completed_onboarding, "Should not be completed initially"
    assert not onboarding_manager.has_seen_tutorial, "Should not have seen tutorial initially"
    assert not onboarding_manager.has_picked_first_color, "Should not have picked first color initially"
    assert onboarding_manager.app_launch_count == 0, "Launch count should be 0"
    print("   ✅ Initial state is correct")


def test_onboarding_completion():
    """Test completing onboarding"""
    print("\n🧪 Testing Onboarding Completion...")
    
    onboarding_manager.reset_all()
    assert not onboarding_manager.has_completed_onboarding
    
    onboarding_manager.complete_onboarding()
    assert onboarding_manager.has_completed_onboarding, "Should be completed after calling complete_onboarding()"
    print("   ✅ Onboarding completion works")


def test_tutorial_completion():
    """Test completing tutorial"""
    print("\n🧪 Testing Tutorial Completion...")
    
    onboarding_manager.reset_all()
    assert not onboarding_manager.has_seen_tutorial
    
    onboarding_manager.complete_tutorial()
    assert onboarding_manager.has_seen_tutorial, "Should have seen tutorial after calling complete_tutorial()"
    print("   ✅ Tutorial completion works")


def test_launch_count():
    """Test launch counting"""
    print("\n🧪 Testing Launch Count...")
    
    onboarding_manager.reset_all()
    assert onboarding_manager.app_launch_count == 0
    
    onboarding_manager.increment_launch_count()
    assert onboarding_manager.app_launch_count == 1
    
    onboarding_manager.increment_launch_count()
    onboarding_manager.increment_launch_count()
    assert onboarding_manager.app_launch_count == 3
    print("   ✅ Launch counting works correctly")


def test_tooltips():
    """Test tooltip tracking"""
    print("\n🧪 Testing Tooltip Tracking...")
    
    onboarding_manager.reset_tooltips()
    
    # Initially no tooltips shown
    assert not onboarding_manager.has_shown_tooltip(TooltipType.CAMERA_PRESS_HOLD)
    assert not onboarding_manager.has_shown_tooltip(TooltipType.CAMERA_AI)
    
    # Mark one as shown
    onboarding_manager.mark_tooltip_shown(TooltipType.CAMERA_PRESS_HOLD)
    assert onboarding_manager.has_shown_tooltip(TooltipType.CAMERA_PRESS_HOLD)
    assert not onboarding_manager.has_shown_tooltip(TooltipType.CAMERA_AI)
    
    # Mark another
    onboarding_manager.mark_tooltip_shown(TooltipType.CAMERA_AI)
    assert onboarding_manager.has_shown_tooltip(TooltipType.CAMERA_AI)
    print("   ✅ Tooltip tracking works correctly")


def test_next_tooltip():
    """Test getting next tooltip for context"""
    print("\n🧪 Testing Next Tooltip Logic...")
    
    onboarding_manager.reset_tooltips()
    
    # First tooltip for camera should be CAMERA_PRESS_HOLD
    next_tip = onboarding_manager.next_tooltip(TooltipContext.CAMERA)
    assert next_tip == TooltipType.CAMERA_PRESS_HOLD, f"Expected CAMERA_PRESS_HOLD, got {next_tip}"
    
    # Mark it as shown
    onboarding_manager.mark_tooltip_shown(TooltipType.CAMERA_PRESS_HOLD)
    
    # Next should be CAMERA_FREEZE
    next_tip = onboarding_manager.next_tooltip(TooltipContext.CAMERA)
    assert next_tip == TooltipType.CAMERA_FREEZE, f"Expected CAMERA_FREEZE, got {next_tip}"
    
    # Mark all camera tooltips
    onboarding_manager.mark_tooltip_shown(TooltipType.CAMERA_FREEZE)
    onboarding_manager.mark_tooltip_shown(TooltipType.CAMERA_AI)
    onboarding_manager.mark_tooltip_shown(TooltipType.CAMERA_COPY)
    
    # Should return None when all shown
    next_tip = onboarding_manager.next_tooltip(TooltipContext.CAMERA)
    assert next_tip is None, f"Expected None when all tooltips shown, got {next_tip}"
    print("   ✅ Next tooltip logic works correctly")


def test_persistence():
    """Test that state persists to disk"""
    print("\n🧪 Testing Persistence...")
    
    # Set some state
    onboarding_manager.reset_all()
    onboarding_manager.complete_onboarding()
    onboarding_manager.increment_launch_count()
    onboarding_manager.mark_tooltip_shown(TooltipType.TOOLS_HARMONY)
    
    # Create a new manager instance (should load from disk)
    new_manager = OnboardingManager()
    
    assert new_manager.has_completed_onboarding, "State should persist to disk"
    assert new_manager.app_launch_count >= 1, "Launch count should persist"
    assert new_manager.has_shown_tooltip(TooltipType.TOOLS_HARMONY), "Tooltips should persist"
    print("   ✅ Persistence works correctly")


def test_version_tracking():
    """Test version tracking"""
    print("\n🧪 Testing Version Tracking...")
    
    onboarding_manager.set_current_version("1.0.0")
    assert onboarding_manager.last_version == "1.0.0"
    assert not onboarding_manager.is_new_version("1.0.0"), "Same version should not be new"
    assert onboarding_manager.is_new_version("2.0.0"), "Different version should be new"
    print("   ✅ Version tracking works correctly")


def test_first_color_pick():
    """Test first color pick tracking"""
    print("\n🧪 Testing First Color Pick...")
    
    onboarding_manager.reset_all()
    assert not onboarding_manager.has_picked_first_color
    
    onboarding_manager.has_picked_first_color = True
    assert onboarding_manager.has_picked_first_color
    print("   ✅ First color pick tracking works")


def test_get_all_status():
    """Test getting all status"""
    print("\n🧪 Testing Get All Status...")
    
    onboarding_manager.reset_all()
    onboarding_manager.complete_onboarding()
    onboarding_manager.increment_launch_count()
    
    status = onboarding_manager.get_all_status()
    
    assert "has_completed_onboarding" in status
    assert "has_seen_tutorial" in status
    assert "has_picked_first_color" in status
    assert "app_launch_count" in status
    assert "shown_tooltips" in status
    assert "last_version" in status
    
    assert status["has_completed_onboarding"] is True
    assert status["app_launch_count"] >= 1
    print("   ✅ Get all status works correctly")


def test_tooltip_properties():
    """Test tooltip type properties"""
    print("\n🧪 Testing Tooltip Properties...")
    
    for tooltip in TooltipType:
        assert tooltip.title, f"{tooltip} should have a title"
        assert tooltip.message, f"{tooltip} should have a message"
        assert tooltip.icon, f"{tooltip} should have an icon"
        print(f"   ✅ {tooltip.name}: {tooltip.title}")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🚀 ColorSnap Pro Onboarding System Tests")
    print("=" * 60)
    
    tests = [
        test_singleton,
        test_initial_state,
        test_onboarding_completion,
        test_tutorial_completion,
        test_launch_count,
        test_tooltips,
        test_next_tooltip,
        test_persistence,
        test_version_tracking,
        test_first_color_pick,
        test_get_all_status,
        test_tooltip_properties,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"   ❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
