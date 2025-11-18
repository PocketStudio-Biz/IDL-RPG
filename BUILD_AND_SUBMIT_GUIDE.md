# IDL RPG - Build and Submission Guide

## Quick Start Checklist

- [ ] Update version and build numbers
- [ ] Clean build folder
- [ ] Archive the app
- [ ] Validate the archive
- [ ] Upload to App Store Connect
- [ ] Complete App Store Connect metadata
- [ ] Submit for review

---

## Step 1: Pre-Build Preparation

### 1.1 Update Version Numbers

**In Xcode:**
1. Select your project in the navigator
2. Select the "IDL RPG iOS" target
3. Go to "General" tab
4. Update:
   - **Version**: `1.0` (Marketing version - user-facing)
   - **Build**: `1` (Build number - increment for each submission)

**Or via project.pbxproj:**
```bash
# Update MARKETING_VERSION and CURRENT_PROJECT_VERSION
```

### 1.2 Verify Bundle Identifier

**Current**: `IDLrpg.IDL-RPG`

**Verify in Xcode:**
- Project → Target → General → Bundle Identifier
- Should match your App Store Connect app record

### 1.3 Check Code Signing

**In Xcode:**
1. Select target → "Signing & Capabilities"
2. Verify:
   - ✅ "Automatically manage signing" is checked
   - Team is selected (VZ77AMNZ8N)
   - Provisioning profile is valid

### 1.4 Remove Debug Code

**Check for:**
- `print()` statements (remove or wrap in `#if DEBUG`)
- Debug UI elements (FPS counter, node count - remove for release)
- Test/development features
- Console logs

**In GameViewController.swift:**
```swift
// Remove or conditionally compile:
skView.showsFPS = true  // Remove for release
skView.showsNodeCount = true  // Remove for release
```

### 1.5 Verify Assets

- [ ] App icon set in Assets.xcassets
- [ ] Launch screen configured
- [ ] All game assets included
- [ ] No missing image references

### 1.6 Check Info.plist Settings

**Verify:**
- App name
- Bundle identifier
- Minimum iOS version (currently 26.1 - may need adjustment to 14.0+)
- Required device capabilities
- Privacy descriptions (if using camera, location, etc.)

### 1.7 Privacy Manifest (iOS 17+)

**Create PrivacyInfo.xcprivacy if not exists:**
- Declare data collection practices
- Required for iOS 17+ apps
- See privacy manifest section below

---

## Step 2: Build Configuration

### 2.1 Select Scheme and Destination

**In Xcode:**
1. **Scheme**: Select "IDL RPG iOS"
2. **Destination**: Select "Any iOS Device" (not simulator)
   - Or select a connected physical device

### 2.2 Build Configuration

**Verify:**
- Configuration: **Release** (not Debug)
- Build Settings → Optimization: **Fastest, Smallest [-Os]**

---

## Step 3: Archive

### 3.1 Create Archive

**Method 1: Xcode GUI**
1. **Product → Archive**
2. Wait for build to complete (may take several minutes)
3. Organizer window opens automatically

**Method 2: Command Line**
```bash
# Navigate to project directory
cd "/Users/mykey/Library/Mobile Documents/com~apple~CloudDocs/WOrkspace/projects/xcode-apple/IDL RPG"

# Clean build folder
xcodebuild clean -scheme "IDL RPG iOS" -configuration Release

# Create archive
xcodebuild archive \
  -scheme "IDL RPG iOS" \
  -configuration Release \
  -archivePath "./build/IDL-RPG.xcarchive" \
  -destination "generic/platform=iOS" \
  CODE_SIGN_IDENTITY="Apple Development" \
  DEVELOPMENT_TEAM="VZ77AMNZ8N"
```

### 3.2 Archive Location

Archives are stored at:
```
~/Library/Developer/Xcode/Archives/[Date]/IDL-RPG [Date], [Time].xcarchive
```

---

## Step 4: Validate Archive

### 4.1 Validate in Xcode

**In Organizer:**
1. Select your archive
2. Click **"Validate App"**
3. Sign in with your Apple ID
4. Review validation results
5. Fix any issues before distributing

**Common Issues:**
- Missing app icon
- Invalid entitlements
- Code signing errors
- Missing privacy manifest
- Invalid bundle identifier

### 4.2 Validate via Command Line

```bash
xcodebuild -validateArchive \
  -archivePath "./build/IDL-RPG.xcarchive"
```

---

## Step 5: Upload to App Store Connect

### 5.1 Upload via Xcode

**In Organizer:**
1. Select your validated archive
2. Click **"Distribute App"**
3. Select **"App Store Connect"**
4. Click **"Next"**
5. Select **"Upload"**
6. Click **"Next"**
7. Review options:
   - ✅ Upload your app's symbols (recommended)
   - ✅ Manage version and build number (if needed)
8. Click **"Next"**
9. Review signing options (usually automatic)
10. Click **"Upload"**
11. Wait for upload to complete

### 5.2 Upload via Transporter

**Alternative method:**
1. Download [Transporter](https://apps.apple.com/us/app/transporter/id1450874784) from Mac App Store
2. Export IPA from Xcode (see Export Options below)
3. Open Transporter
4. Drag IPA file into Transporter
5. Sign in and upload

### 5.3 Export Options (for Transporter)

**Create ExportOptions.plist:**
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
    <key>destination</key>
    <string>upload</string>
</dict>
</plist>
```

**Export via command line:**
```bash
xcodebuild -exportArchive \
  -archivePath "./build/IDL-RPG.xcarchive" \
  -exportPath "./build" \
  -exportOptionsPlist ExportOptions.plist
```

---

## Step 6: App Store Connect Setup

### 6.1 Create App Record (First Time Only)

1. Go to [App Store Connect](https://appstoreconnect.apple.com)
2. Click **"My Apps"**
3. Click **"+"** → **"New App"**
4. Fill in:
   - **Platform**: iOS
   - **Name**: IDL RPG
   - **Primary Language**: English (U.S.)
   - **Bundle ID**: IDLrpg.IDL-RPG
   - **SKU**: IDL-RPG-001
5. Click **"Create"**

### 6.2 Wait for Build Processing

**After upload:**
- Build appears in "TestFlight" tab first
- Processing takes 15-60 minutes typically
- Status: "Processing" → "Ready to Submit"

**Check status:**
- App Store Connect → Your App → TestFlight → iOS Builds

### 6.3 Complete App Information

**Go to App Store tab:**

1. **App Information**
   - Category: Games → Role Playing
   - Content Rights: Confirm you have rights
   - Age Rating: Complete questionnaire

2. **Pricing and Availability**
   - Price: Free
   - Availability: All countries (or select)

3. **Version Information**
   - What's New: (See APP_STORE_METADATA.md)
   - Description: (See APP_STORE_METADATA.md)
   - Keywords: (See APP_STORE_METADATA.md)
   - Support URL: Your support page
   - Marketing URL: (Optional)
   - Privacy Policy URL: **REQUIRED**

4. **App Preview and Screenshots**
   - Upload screenshots for all required sizes
   - See screenshot requirements below

### 6.4 Select Build

1. Go to **"Version Information"**
2. Under **"Build"**, click **"+ Version or Platform"**
3. Select your processed build
4. Click **"Done"**

---

## Step 7: Submit for Review

### 7.1 Final Checklist

- [ ] All metadata completed
- [ ] Screenshots uploaded
- [ ] Privacy policy URL added
- [ ] Build selected
- [ ] Export compliance answered
- [ ] Review notes added (optional)

### 7.2 Export Compliance

**Answer questions:**
- Uses encryption? Usually "No" for games
- Uses standard encryption? Usually "No"
- If yes, provide encryption details

### 7.3 Submit

1. Click **"Add for Review"** or **"Submit for Review"**
2. Review submission checklist
3. Click **"Submit"**
4. Status changes to **"Waiting for Review"**

---

## Step 8: Monitor Review

### 8.1 Review Statuses

- **Waiting for Review**: In queue
- **In Review**: Being reviewed (24-48 hours typically)
- **Pending Developer Release**: Approved, waiting for you
- **Ready for Sale**: Live on App Store
- **Rejected**: Issues found (check Resolution Center)

### 8.2 Check Status

**App Store Connect → Your App → App Store → [Version]**

### 8.3 Respond to Feedback

**If Rejected:**
1. Check **"Resolution Center"** for details
2. Read rejection reasons carefully
3. Fix issues
4. Resubmit with explanation

**If Approved:**
1. App goes live (if set to automatic release)
2. Or manually release when ready
3. Monitor for issues

---

## Privacy Manifest (iOS 17+)

### Create PrivacyInfo.xcprivacy

**Location**: Add to "IDL RPG iOS" target

**Content** (example for no data collection):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
    <key>NSPrivacyCollectedDataTypes</key>
    <array/>
    <key>NSPrivacyAccessedAPITypes</key>
    <array/>
</dict>
</plist>
```

**Add to Xcode:**
1. File → New → File
2. iOS → Resource → Privacy Manifest File
3. Name: `PrivacyInfo.xcprivacy`
4. Add to "IDL RPG iOS" target

---

## Screenshot Requirements

### Required Sizes

**iPhone:**
- 6.7" (iPhone 14 Pro Max, 15 Pro Max): 1290 x 2796 px
- 6.5" (iPhone 11 Pro Max, XS Max): 1242 x 2688 px
- 5.5" (iPhone 8 Plus): 1242 x 2208 px

**iPad:**
- 12.9" (iPad Pro): 2048 x 2732 px
- 11" (iPad Pro): 1668 x 2388 px

### Creating Screenshots

**Method 1: Simulator**
1. Run app in iOS Simulator
2. Cmd+S to take screenshot
3. Screenshots saved to Desktop

**Method 2: Device**
1. Run app on physical device
2. Take screenshot (Power + Volume Up)
3. Transfer to Mac

**Method 3: Design Tools**
- Create mockups in Figma/Sketch
- Export at required sizes

---

## Troubleshooting

### Build Errors

**"Code signing error"**
- Check team selection
- Verify certificates are valid
- Clean build folder and try again

**"Missing app icon"**
- Verify AppIcon in Assets.xcassets
- Check all required sizes are present

**"Invalid bundle identifier"**
- Must match App Store Connect app record
- Check for typos

### Upload Errors

**"Invalid binary"**
- Check minimum iOS version
- Verify architecture (arm64)
- Check for private API usage

**"Processing failed"**
- Wait and try again
- Check App Store Connect status page
- Contact Apple Developer Support if persistent

---

## Version Management

### Version Numbering

**Format**: `MAJOR.MINOR.PATCH`
- **Major**: Breaking changes
- **Minor**: New features
- **Patch**: Bug fixes

**Examples:**
- 1.0.0 - Initial release
- 1.0.1 - Bug fix
- 1.1.0 - New features
- 2.0.0 - Major update

### Build Number

- Increment for **every** submission
- Even if version doesn't change
- Can be any number (1, 2, 3... or date-based)

---

## Quick Reference Commands

```bash
# Clean
xcodebuild clean -scheme "IDL RPG iOS"

# Archive
xcodebuild archive -scheme "IDL RPG iOS" -configuration Release

# List archives
ls ~/Library/Developer/Xcode/Archives/

# Validate
xcodebuild -validateArchive -archivePath "path/to/archive"

# Export
xcodebuild -exportArchive -archivePath "path/to/archive" -exportOptionsPlist ExportOptions.plist
```

---

**Last Updated**: [Date]

