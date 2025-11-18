# IDL RPG - App Store Submission Plan

## Step 1: Define Requirements

### App Information
- **App Name**: IDL RPG (Idle RPG)
- **Bundle Identifier**: IDLrpg.IDL-RPG
- **Current Version**: 1.0
- **Marketing Version**: 1.0

### Target Platforms
- **Primary**: iOS (iPhone & iPad)
- **Secondary**: macOS (Catalyst/Universal)
- **Minimum iOS Version**: iOS 14.0+ (Note: Project currently set to 26.1, needs adjustment)
- **Device Support**: iPhone and iPad (Universal)

### Core Features
1. **Auto-Battle System**
   - Automatic combat calculations
   - Damage formulas and stat-based combat
   - Real-time battle visualization with SpriteKit

2. **Character Progression**
   - Player stats (HP, Attack, Defense, etc.)
   - Leveling system with XP curves
   - Equipment system (weapons, armor)
   - Stat growth and upgrades

3. **Idle Mechanics**
   - Offline progression calculation
   - Reward caps for balance
   - Background progression tracking

4. **Save/Load System**
   - Persistent game state
   - CoreData/UserDefaults integration
   - Cloud sync capability (future)

5. **Equipment & Inventory**
   - Equipment management
   - Upgrade system
   - Loot tables and rewards

6. **Battle Visualization**
   - SpriteKit animations
   - Particle effects
   - Combat feedback

### Unique Selling Points (USPs)
1. **True Idle Gameplay**: Progress even when the app is closed
2. **Offline-First Design**: No internet required for core gameplay
3. **Deep Progression**: Meaningful character and equipment upgrades
4. **Smooth Animations**: 60fps SpriteKit-based combat visuals
5. **Cross-Platform**: iOS and macOS support

### Technical Requirements
- **Architecture**: MVVM with Combine
- **Performance**: 60fps target, <100ms save/load
- **Size**: <50MB initial download
- **Accessibility**: VoiceOver and Dynamic Type support
- **Privacy**: Privacy manifest compliance

---

## Step 2: Establish Design Guidelines

### Color Palette
- **Primary Color**: #3451E5 (Royal Blue)
- **Secondary Color**: #2C3E50 (Dark Blue-Gray)
- **Accent Color**: #E74C3C (Red for damage/combat)
- **Success Color**: #27AE60 (Green for rewards/upgrades)
- **Background**: #1A1A2E (Dark Navy)
- **Text Primary**: #FFFFFF (White)
- **Text Secondary**: #B0B0B0 (Light Gray)

### Typography
- **Primary Font**: SF Pro (System Font)
- **Game Font**: Custom pixel/retro font for game UI (optional)
- **Headings**: Bold, 24-32pt
- **Body**: Regular, 16-18pt
- **Small Text**: Regular, 12-14pt

### UI/UX Specifications
- **Layout**: Card-based design with rounded corners
- **Spacing**: 16pt standard padding, 8pt tight spacing
- **Corner Radius**: 12pt for cards, 8pt for buttons
- **Shadows**: Subtle elevation for depth
- **Animations**: 0.3s standard transitions

### App Icon Requirements
- **Size**: 1024x1024px (App Store)
- **Format**: PNG with transparency
- **Style**: 
  - Game character or RPG symbol
  - Vibrant colors matching brand
  - Recognizable at small sizes
  - No text (Apple requirement)

### Screenshot Specifications
**Required Sizes:**
- iPhone 6.7" (iPhone 14 Pro Max, 15 Pro Max): 1290 x 2796 px
- iPhone 6.5" (iPhone 11 Pro Max, XS Max): 1242 x 2688 px
- iPhone 5.5" (iPhone 8 Plus): 1242 x 2208 px
- iPad Pro 12.9": 2048 x 2732 px
- iPad Pro 11": 1668 x 2388 px

**Screenshot Content:**
1. Main battle screen with character and enemy
2. Character stats and progression screen
3. Equipment/inventory management
4. Upgrade/shop interface
5. Idle rewards collection screen

**Screenshot Folder**: `./AppStoreAssets/Screenshots/`

---

## Step 3: Code Development Phases

### Module Structure
```
IDL RPG/
├── Models/
│   ├── Player.swift
│   ├── Enemy.swift
│   ├── Equipment.swift
│   ├── GameState.swift
│   └── Progression.swift
├── ViewModels/
│   ├── GameViewModel.swift
│   ├── BattleViewModel.swift
│   ├── CharacterViewModel.swift
│   └── ShopViewModel.swift
├── Views/
│   ├── MainGameView.swift
│   ├── BattleView.swift
│   ├── CharacterView.swift
│   └── ShopView.swift
├── Services/
│   ├── BattleSystem.swift
│   ├── ProgressionSystem.swift
│   ├── IdleCalculator.swift
│   ├── SaveManager.swift
│   └── GameStateManager.swift
└── Utilities/
    ├── Extensions.swift
    └── Constants.swift
```

### Development Phases

**Phase 1: Foundation (Current)**
- [x] Basic SpriteKit setup
- [ ] MVVM architecture implementation
- [ ] Core data models
- [ ] Service layer setup

**Phase 2: Core Systems**
- [ ] Battle system implementation
- [ ] Progression system
- [ ] Save/load functionality
- [ ] Idle calculator

**Phase 3: UI Implementation**
- [ ] SwiftUI main interface
- [ ] Battle visualization
- [ ] Character management UI
- [ ] Shop/upgrade interface

**Phase 4: Polish & Testing**
- [ ] Animations and effects
- [ ] Accessibility features
- [ ] Performance optimization
- [ ] Unit and UI tests

**Phase 5: App Store Prep**
- [ ] Privacy policy
- [ ] App Store metadata
- [ ] Screenshots
- [ ] Build configuration

### Repository Structure
- **Main Branch**: `main` (production-ready)
- **Development Branch**: `develop`
- **Feature Branches**: `feature/[module-name]`
- **Release Branches**: `release/v[version]`

---

## Step 4: Testing Plan

### Testing Stack
- **Unit Testing**: XCTest
- **UI Testing**: XCUITest
- **Performance Testing**: XCTest Performance Metrics
- **Accessibility Testing**: VoiceOver, Dynamic Type

### Unit Tests
**Target Coverage**: 80%+ for core systems

**Test Suites:**
1. **BattleSystemTests**
   - Damage calculation accuracy
   - Stat modifiers
   - Combat outcomes

2. **ProgressionSystemTests**
   - XP curve calculations
   - Level-up logic
   - Stat growth formulas

3. **IdleCalculatorTests**
   - Offline time calculations
   - Reward caps
   - Edge cases (negative time, very long offline)

4. **SaveManagerTests**
   - Save/load functionality
   - Data integrity
   - Migration scenarios

5. **GameStateManagerTests**
   - State transitions
   - Data consistency
   - Error handling

### Integration Tests
- **Game Flow Tests**: Complete gameplay cycles
- **Save/Load Integration**: Persistence across app launches
- **Idle Progression**: Offline reward calculation accuracy

### UI Tests
1. **Navigation Tests**
   - Screen transitions
   - Tab navigation
   - Modal presentations

2. **Interaction Tests**
   - Button taps
   - Equipment selection
   - Upgrade purchases

3. **Accessibility Tests**
   - VoiceOver navigation
   - Dynamic Type scaling
   - Color contrast compliance

### Performance Tests
- **Frame Rate**: Maintain 60fps during combat
- **Save/Load Time**: <100ms for save operations
- **Memory Usage**: Monitor for leaks
- **Startup Time**: <2 seconds to first screen

### Test Execution
```bash
# Run all tests
xcodebuild test -scheme "IDL RPG iOS" -destination 'platform=iOS Simulator,name=iPhone 15'

# Run specific test suite
xcodebuild test -scheme "IDL RPG iOS" -only-testing:IDLRPGTests/BattleSystemTests

# Generate coverage report
xcodebuild test -scheme "IDL RPG iOS" -enableCodeCoverage YES
```

---

## Step 5: Prepare App Store Listing

### App Store Metadata

#### App Name
**IDL RPG** (30 characters max)

#### Subtitle
**Idle Adventure RPG** (30 characters max)

#### Description
```
Embark on an epic idle RPG adventure where your hero fights automatically, even when you're away!

🎮 AUTOMATIC COMBAT
Watch your character battle enemies automatically with smooth, real-time animations. No need to tap constantly - just set your strategy and let the game play!

⚔️ DEEP PROGRESSION
Level up your hero, equip powerful weapons and armor, and unlock new abilities. Every upgrade matters as you progress through increasingly challenging enemies.

💰 OFFLINE REWARDS
Close the app and come back later to collect rewards! Your hero continues fighting even when you're not playing, with balanced reward caps to keep progression fair.

🎯 STRATEGIC UPGRADES
Choose your equipment wisely. Different weapons and armor provide unique stat bonuses that can dramatically change your combat effectiveness.

✨ SMOOTH ANIMATIONS
Experience beautiful SpriteKit-powered combat animations at 60fps. Every battle feels impactful with particle effects and visual feedback.

🌟 FEATURES:
• Automatic idle combat system
• Deep character progression with levels and stats
• Equipment system with upgrades
• Offline progression and rewards
• Beautiful battle animations
• No internet required for core gameplay
• Optimized for iPhone and iPad

Perfect for RPG fans who want meaningful progression without constant attention. Start your idle adventure today!
```

#### Keywords
```
idle,rpg,adventure,game,automatic,battle,progression,offline,character,equipment,upgrade,strategy,hero,fantasy
```
(100 characters max, comma-separated, no spaces after commas)

#### Support URL
```
https://idlrpg.com/support
```
(Or your support page URL)

#### Marketing URL (Optional)
```
https://idlrpg.com
```

#### Privacy Policy URL
```
https://idlrpg.com/privacy
```
**REQUIRED** - See Privacy Policy section below

#### Category
- **Primary**: Games
- **Secondary**: Role Playing

#### Age Rating
- **Content Rating**: 4+ (Everyone)
- **Justification**: No violence, no objectionable content, fantasy combat only

#### Pricing
- **Price**: Free
- **In-App Purchases**: None (initially)
- **Future IAP Options**: 
  - Remove ads (if added)
  - Cosmetic items
  - Premium currency (optional)

### Privacy Policy Template

Create file: `PRIVACY_POLICY.md` (see separate file)

**Key Points:**
- No data collection
- No third-party analytics (or disclose if used)
- No user accounts required
- Local data storage only
- No sharing of personal information

### App Store Screenshots Guide

**Screenshot 1: Main Battle Screen**
- Show character fighting enemy
- Display level, HP, damage numbers
- Highlight automatic combat

**Screenshot 2: Character Progression**
- Show stats screen
- Display equipment
- Highlight level and XP

**Screenshot 3: Equipment & Upgrades**
- Show inventory/equipment screen
- Display upgrade options
- Highlight stat improvements

**Screenshot 4: Idle Rewards**
- Show offline rewards collection
- Display time away and rewards earned
- Highlight idle progression

**Screenshot 5: Battle Animation**
- Show combat in action
- Display particle effects
- Highlight visual polish

### App Preview Video (Optional)
- 15-30 seconds
- Show gameplay highlights
- Auto-battle, upgrades, progression
- Add text overlays for key features

---

## Step 6: Build & Archive Release

### Build Configuration

#### Release Build Settings
1. **Scheme**: "IDL RPG iOS"
2. **Configuration**: Release
3. **Code Signing**: Automatic (with your team)
4. **Bitcode**: Enabled (if supported)
5. **Optimization**: Fastest, Smallest [-Os]

#### Pre-Build Checklist
- [ ] Update version number in project settings
- [ ] Update build number
- [ ] Verify bundle identifier
- [ ] Check code signing certificates
- [ ] Remove debug code and print statements
- [ ] Disable test/development features
- [ ] Verify all assets are included
- [ ] Check Info.plist settings
- [ ] Verify privacy manifest (PrivacyInfo.xcprivacy)

#### Archive Process
1. **Open Xcode**
2. **Select Scheme**: "IDL RPG iOS"
3. **Select Destination**: "Any iOS Device" or specific device
4. **Product → Archive**
5. **Wait for build to complete**
6. **Organizer window opens automatically**

#### Archive Verification
1. **Validate Archive**
   - Click "Validate App" in Organizer
   - Fix any issues before distribution
   - Check for common issues:
     - Missing icons
     - Invalid entitlements
     - Code signing errors
     - Missing privacy manifest

2. **Export for App Store**
   - Click "Distribute App"
   - Select "App Store Connect"
   - Choose distribution method
   - Upload to App Store Connect

#### Build Commands (Alternative)
```bash
# Clean build folder
xcodebuild clean -scheme "IDL RPG iOS"

# Archive
xcodebuild archive \
  -scheme "IDL RPG iOS" \
  -configuration Release \
  -archivePath "./build/IDL-RPG.xcarchive" \
  -destination "generic/platform=iOS"

# Export IPA (requires export options plist)
xcodebuild -exportArchive \
  -archivePath "./build/IDL-RPG.xcarchive" \
  -exportPath "./build" \
  -exportOptionsPlist ExportOptions.plist
```

### Export Options Plist
Create `ExportOptions.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>VZ77AMNZ8N</string>
    <key>uploadBitcode</key>
    <true/>
    <key>uploadSymbols</key>
    <true/>
    <key>compileBitcode</key>
    <true/>
</dict>
</plist>
```

### Version Management
- **Marketing Version**: User-facing version (e.g., 1.0.0)
- **Build Number**: Increment for each submission (e.g., 1, 2, 3...)
- **Update both** before each App Store submission

---

## Step 7: Submit to Store

### App Store Connect Setup

#### 1. Create App Record
- Log into [App Store Connect](https://appstoreconnect.apple.com)
- Go to "My Apps" → "+" → "New App"
- Fill in:
  - **Platform**: iOS
  - **Name**: IDL RPG
  - **Primary Language**: English (U.S.)
  - **Bundle ID**: IDLrpg.IDL-RPG
  - **SKU**: IDL-RPG-001 (unique identifier)

#### 2. App Information
- **Category**: Games → Role Playing
- **Content Rights**: Confirm you have rights to all content
- **Age Rating**: Complete questionnaire (should result in 4+)

#### 3. Pricing and Availability
- **Price**: Free
- **Availability**: All countries (or select specific)
- **Pre-Order**: No

#### 4. Prepare for Submission
Fill in all required fields:

**Version Information:**
- **What's New**: First release notes
- **Description**: (From Step 5)
- **Keywords**: (From Step 5)
- **Support URL**: Your support page
- **Marketing URL**: (Optional)
- **Privacy Policy URL**: (Required)

**App Preview and Screenshots:**
- Upload screenshots for all required device sizes
- Add app preview video (optional but recommended)

**Build:**
- Upload build via Xcode or Transporter
- Wait for processing (can take 15-60 minutes)
- Select processed build for submission

**Version Release:**
- **Automatic**: Release immediately after approval
- **Manual**: Release when you choose
- **Scheduled**: Set specific date/time

#### 5. Submit for Review
- Complete all required information
- Answer export compliance questions
- Submit for review

### Submission Checklist
- [ ] App Store Connect app record created
- [ ] All metadata filled in
- [ ] Screenshots uploaded for all sizes
- [ ] Privacy policy URL added
- [ ] Build uploaded and processed
- [ ] Build selected for submission
- [ ] Export compliance answered
- [ ] Review notes added (if needed)
- [ ] Contact information verified
- [ ] Submitted for review

### Review Notes (Optional but Recommended)
```
Thank you for reviewing IDL RPG!

This is an idle RPG game where players progress automatically. Key features:
- Automatic combat system (no constant tapping required)
- Offline progression with reward caps
- Character leveling and equipment upgrades
- No user accounts or data collection required
- All gameplay is local, no internet connection needed

If you have any questions or need additional information, please contact us at [your-email@example.com].

Test Account (if applicable): N/A - No login required
```

### Expected Review Timeline
- **Initial Review**: 24-48 hours typically
- **Re-review** (if rejected): 24-48 hours after resubmission
- **Total Time**: 1-7 days typically

---

## Step 8: Post-Submission

### Monitor Review Status

#### App Store Connect Dashboard
1. **Check Status Regularly**
   - "Waiting for Review"
   - "In Review"
   - "Pending Developer Release"
   - "Ready for Sale"
   - "Rejected" (if issues found)

2. **Review Feedback**
   - Check "Resolution Center" for messages
   - Read rejection reasons carefully
   - Address all issues before resubmitting

### Common Rejection Reasons & Solutions

#### 1. Missing Privacy Policy
**Solution**: Add privacy policy URL in App Store Connect

#### 2. App Crashes
**Solution**: 
- Test on multiple devices
- Fix crashes and resubmit
- Add crash reporting (e.g., Firebase Crashlytics)

#### 3. Missing Functionality
**Solution**: Ensure all features mentioned in description work

#### 4. Guideline Violations
**Solution**: Review App Store Review Guidelines and fix issues

#### 5. Metadata Issues
**Solution**: Ensure screenshots match app functionality

### Responding to Feedback

#### If Approved
1. **Celebrate!** 🎉
2. **Monitor Launch**:
   - Watch for crashes
   - Monitor user reviews
   - Track analytics (if implemented)

#### If Rejected
1. **Read Rejection Carefully**
2. **Identify Root Cause**
3. **Fix Issues**:
   - Update code if needed
   - Fix metadata if needed
   - Update screenshots if needed
4. **Resubmit** with explanation of fixes
5. **Appeal** if you believe rejection is incorrect

### Post-Launch Monitoring

#### Key Metrics to Track
- **Downloads**: Track daily/weekly downloads
- **Ratings**: Monitor App Store ratings
- **Reviews**: Read and respond to user reviews
- **Crashes**: Monitor crash reports
- **Performance**: Track app performance metrics

#### User Feedback Response
- **Respond to Reviews**: Thank users, address concerns
- **Update Frequently**: Fix bugs, add features
- **Communicate**: Let users know about updates

### Update Process
1. **Make Changes**: Fix bugs, add features
2. **Update Version**: Increment version number
3. **Test Thoroughly**: Ensure no regressions
4. **Archive & Upload**: Follow Step 6 process
5. **Update Metadata**: Add "What's New" notes
6. **Submit Update**: Follow Step 7 process

### Hotfix Process
For critical bugs:
1. **Identify Issue**: Reproduce and fix
2. **Fast-Track Build**: Expedite testing
3. **Submit Update**: Mark as urgent if needed
4. **Communicate**: Update users via App Store notes

---

## Additional Resources

### Apple Documentation
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [App Store Connect Help](https://help.apple.com/app-store-connect/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

### Tools
- **Xcode**: Primary development tool
- **App Store Connect**: Submission and management
- **Transporter**: Alternative upload tool
- **TestFlight**: Beta testing (optional but recommended)

### Support Contacts
- **Apple Developer Support**: [developer.apple.com/contact](https://developer.apple.com/contact)
- **App Review Board**: Via App Store Connect Resolution Center

---

## Checklist Summary

### Pre-Submission
- [ ] All features implemented and tested
- [ ] Privacy policy created and hosted
- [ ] Screenshots created for all device sizes
- [ ] App Store metadata prepared
- [ ] Build archived and validated
- [ ] Code signing configured correctly

### Submission
- [ ] App Store Connect app record created
- [ ] All metadata entered
- [ ] Screenshots uploaded
- [ ] Build uploaded and selected
- [ ] Submitted for review

### Post-Submission
- [ ] Monitoring review status
- [ ] Ready to respond to feedback
- [ ] Post-launch monitoring plan in place

---

**Last Updated**: [Current Date]
**Version**: 1.0
**Status**: Ready for Implementation

