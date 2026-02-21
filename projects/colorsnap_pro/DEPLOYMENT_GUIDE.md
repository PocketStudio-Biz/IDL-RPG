# 🚀 ColorSnap Pro - Deployment Guide

Complete guide for deploying ColorSnap Pro to TestFlight (iOS) and distributing the Python desktop app.

---

## 📱 iOS - TestFlight Deployment

### Prerequisites

- [Xcode 15+](https://developer.apple.com/xcode/) installed
- Apple Developer Account ($99/year)
- App Store Connect access

### Step 1: Archive the App

```bash
cd /Users/mykey/projects/colorsnap_pro/ios-app

# Clean build
xcodebuild clean -project ColorSnapPro.xcodeproj -scheme ColorSnapPro

# Archive for distribution
xcodebuild archive \
  -project ColorSnapPro.xcodeproj \
  -scheme ColorSnapPro \
  -archivePath ColorSnapPro.xcarchive \
  -destination 'generic/platform=iOS'
```

### Step 2: Upload to App Store Connect

**Option A: Via Xcode Organizer**
1. Open Xcode
2. Window → Organizer
3. Select the archive
4. Click "Distribute App"
5. Select "App Store Connect"
6. Choose "Upload"
7. Follow prompts (signing, etc.)

**Option B: Via Command Line**

```bash
# Export options plist
cat > export_options.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadBitcode</key>
    <false/>
    <key>uploadSymbols</key>
    <true/>
</dict>
</plist>
EOF

# Export IPA
xcodebuild -exportArchive \
  -archivePath ColorSnapPro.xcarchive \
  -exportOptionsPlist export_options.plist \
  -exportPath ./build

# Upload using altool
xcrun altool --upload-app \
  --type ios \
  --file "build/ColorSnapPro.ipa" \
  --apiKey YOUR_API_KEY \
  --apiIssuer YOUR_ISSUER_ID
```

### Step 3: Generate Screenshots

**Using Fastlane (Recommended):**

```bash
# Install fastlane
sudo gem install fastlane

# Initialize fastlane (if not done)
fastlane init

# Take screenshots on all devices
fastlane snapshot

# Frame screenshots (optional)
fastlane frameit
```

**Manual Screenshots:**
1. Run app on different simulators
2. Cmd+S to save screenshots
3. Organize by device size

### Step 4: Configure App Store Connect

1. Go to [App Store Connect](https://appstoreconnect.apple.com)
2. Click "My Apps"
3. Create new app:
   - **Platforms:** iOS
   - **Name:** ColorSnap Pro
   - **Bundle ID:** com.mykey.colorsnappro
   - **SKU:** colorsnappro-001
4. Fill in:
   - **App Information:** Category, description
   - **Pricing:** Free or paid
   - **Screenshots:** Upload for all device sizes
   - **App Preview:** Optional video

### Step 5: Enable TestFlight

1. In App Store Connect, go to "TestFlight" tab
2. Internal Testing:
   - Add your Apple ID email
   - Select the build
   - Add testers
3. External Testing (optional):
   - Create a group
   - Submit for beta review
   - Share public link

### Step 6: Install from TestFlight

1. Download [TestFlight app](https://apps.apple.com/us/app/testflight/id899247664)
2. Accept invitation (via email or link)
3. Tap "Install" for ColorSnap Pro

---

## 🐍 Python Desktop - Distribution

### Prerequisites

```bash
cd /Users/mykey/projects/colorsnap_pro/python_onboarding

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Build Options

#### Option 1: Simple Executable (All Platforms)

```bash
# One folder (recommended)
python build_app.py

# Or one single file
python build_app.py --onefile
```

#### Option 2: macOS App Bundle + DMG

```bash
# Build app bundle
python build_app.py

# Create DMG for distribution
cd dist

# Using create-dmg (install with: brew install create-dmg)
create-dmg \
  --volname "ColorSnap Pro" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --app-drop-link 450 185 \
  "ColorSnapPro-1.0.0.dmg" \
  "ColorSnapPro.app"
```

#### Option 3: Windows Installer

```bash
# On Windows, with Inno Setup installed:
python build_app.py --installer

# Or manually:
python build_app.py
# Then use Inno Setup to create installer
```

#### Option 4: Linux AppImage

```bash
# On Linux, with appimagetool installed:
python build_app.py --appimage
```

### Complete Build (All Platforms)

```bash
python build_app.py --all
```

### Distribution Platforms

#### itch.io

1. Create account at [itch.io](https://itch.io)
2. Create new project
3. Upload:
   - macOS: `ColorSnapPro-1.0.0.dmg`
   - Windows: `ColorSnapPro-1.0.0-Setup.exe`
   - Linux: `ColorSnapPro-1.0.0-x86_64.AppImage`
4. Set pricing or make free
5. Publish

#### GitHub Releases

```bash
# Create release tag
git tag -a v1.0.0 -m "ColorSnap Pro v1.0.0"
git push origin v1.0.0

# Go to GitHub → Releases → Create Release
# Upload all build artifacts
```

#### Direct Download

Host files on:
- AWS S3
- Google Cloud Storage
- Personal website
- Dropbox (direct links)

---

## 📸 Screenshot Automation

### iOS Screenshots

```bash
cd /Users/mykey/projects/colorsnap_pro/ios-app

# Run automated screenshots
fastlane snapshot

# Screenshot locations:
# ./fastlane/screenshots/en-US/
```

### Python Screenshots

```bash
cd /Users/mykey/projects/colorsnap_pro/python_onboarding

# Run screenshot tool
python screenshot_tool.py

# Or programmatically:
from screenshot_tool import capture_app_screenshots
capture_app_screenshots(main_window, "~/screenshots")
```

---

## ✅ Pre-Release Checklist

### iOS

- [ ] Build succeeds with no warnings
- [ ] App launches on physical device
- [ ] Camera permissions work
- [ ] All features tested
- [ ] Screenshots generated
- [ ] App Store metadata complete
- [ ] Privacy manifest included
- [ ] Archive uploaded
- [ ] TestFlight build processed

### Python

- [ ] App runs without errors
- [ ] All features working
- [ ] Executable builds successfully
- [ ] Test on clean machine (no Python installed)
- [ ] Icons and metadata included
- [ ] README included
- [ ] Screenshots captured
- [ ] Distribution package created

---

## 🚨 Common Issues

### iOS

**Issue:** "No signing certificate found"
- **Fix:** Xcode → Preferences → Accounts → Download Manual Profiles

**Issue:** "Bundle identifier not available"
- **Fix:** Change bundle ID in project settings

**Issue:** "Asset validation failed"
- **Fix:** Ensure 1024x1024 app icon is included

### Python

**Issue:** "PyInstaller not found"
- **Fix:** `pip install pyinstaller`

**Issue:** "App won't open on macOS"
- **Fix:** Right-click → Open, or codesign: `codesign --force --deep --sign - ColorSnapPro.app`

**Issue:** "Windows Defender flags app"
- **Fix:** Submit to Microsoft for analysis, or use code signing certificate

---

## 📞 Support

- **iOS Issues:** [Apple Developer Forums](https://developer.apple.com/forums/)
- **Python Build Issues:** [PyInstaller Issues](https://github.com/pyinstaller/pyinstaller/issues)
- **TestFlight Issues:** [App Store Connect Help](https://help.apple.com/app-store-connect/)

---

## 🎉 Release Timeline

| Step | iOS | Python |
|------|-----|--------|
| Build | 2 min | 2 min |
| Screenshots | 10 min | 5 min |
| Upload | 5 min | 1 min |
| Processing | 10-30 min | Instant |
| **Total** | **30-50 min** | **10 min** |

**Good luck with your launch! 🚀**
