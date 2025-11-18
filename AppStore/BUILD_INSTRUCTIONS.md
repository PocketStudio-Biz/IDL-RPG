# Build and Archive Instructions for IDL RPG

## Prerequisites

1. **Xcode** - Latest version recommended (Xcode 26.1+ based on project settings)
2. **Apple Developer Account** - Active membership with Team ID: `VZ77AMNZ8N`
3. **Code Signing Certificates** - Distribution certificates installed in Keychain
4. **Provisioning Profiles** - App Store distribution profiles configured

## Pre-Build Checklist

- [x] Deployment targets fixed:
  - iOS: 15.0
  - macOS: 11.0
- [x] Debug overlays disabled in release builds
- [x] Bundle identifier: `IDLrpg.IDL-RPG`
- [ ] Increment build number (if resubmitting)
- [ ] Verify all assets are included
- [ ] Test on physical device (iOS)
- [ ] Test on macOS

## iOS Build Process

### Step 1: Configure Build Settings

1. Open `IDL RPG.xcodeproj` in Xcode
2. Select the project in the navigator
3. Select the "IDL RPG iOS" target
4. Go to "Signing & Capabilities" tab
5. Verify:
   - Team: `VZ77AMNZ8N` (or your team name)
   - Bundle Identifier: `IDLrpg.IDL-RPG`
   - Provisioning Profile: Automatic (or select App Store profile)
6. Go to "Build Settings" tab
7. Verify:
   - Code Signing Style: Automatic
   - Development Team: VZ77AMNZ8N
   - iOS Deployment Target: 15.0

### Step 2: Create Archive

1. In Xcode menu: **Product > Destination > Any iOS Device**
   - Alternatively: Select "Generic iOS Device" from the device selector
2. **Product > Scheme > IDL RPG iOS** (if not already selected)
3. **Product > Archive**
4. Wait for the build to complete (may take several minutes)
5. The Organizer window should open automatically when archive completes

### Step 3: Validate Archive

1. In the Organizer window, select your archive
2. Click **Validate App**
3. Select distribution method: **App Store Connect**
4. Click **Next**
5. Review validation options:
   - Automatically manage signing: Checked (recommended)
   - Include bitcode: Optional (iOS)
6. Click **Validate**
7. Wait for validation to complete
8. Review any warnings or errors:
   - Fix any critical errors
   - Address warnings as needed
   - Non-critical warnings may not block submission

### Step 4: Distribute to App Store Connect

1. In the Organizer, select your validated archive
2. Click **Distribute App**
3. Select **App Store Connect**
4. Click **Next**
5. Select distribution method:
   - **Upload**: Uploads to App Store Connect immediately (recommended)
   - **Export**: Saves .ipa file for manual upload later
6. Select options:
   - **Include bitcode**: Optional
   - **Upload your app's symbols**: Recommended for crash reporting
7. Click **Next**
8. Select distribution certificate and provisioning profile
9. Click **Upload**
10. Wait for upload to complete
11. Note the build number that was uploaded

## macOS Build Process

### Step 1: Configure Build Settings

1. Select the "IDL RPG macOS" target
2. Go to "Signing & Capabilities" tab
3. Verify:
   - Team: `VZ77AMNZ8N`
   - Bundle Identifier: `IDLrpg.IDL-RPG`
   - Provisioning Profile: Automatic
4. Go to "Build Settings" tab
5. Verify:
   - macOS Deployment Target: 11.0
   - Hardened Runtime: Enabled
   - App Sandbox: Enabled

### Step 2: Create Archive

1. In Xcode menu: **Product > Destination > Any Mac**
2. **Product > Scheme > IDL RPG macOS** (if not already selected)
3. **Product > Archive**
4. Wait for the build to complete

### Step 3: Validate and Distribute

1. Follow the same validation and distribution steps as iOS
2. Note: macOS apps may require additional entitlements review

## Troubleshooting

### Common Build Errors

**Code Signing Issues:**
- Error: "No profiles for 'IDLrpg.IDL-RPG' were found"
  - Solution: Ensure App Store distribution profile exists in developer portal
  - Solution: Verify bundle identifier matches exactly

**Deployment Target Errors:**
- Error: "IPHONEOS_DEPLOYMENT_TARGET is set to..."
  - Solution: Verify deployment target is 15.0 (not 26.1)
  - Check all build configurations (Debug and Release)

**Archive Errors:**
- Error: "No such module" or missing dependencies
  - Solution: Clean build folder (Product > Clean Build Folder)
  - Solution: Reset package caches if using Swift Package Manager

### Validation Warnings

**Missing Privacy Manifest:**
- The PrivacyInfo.xcprivacy file is included in the shared folder
- Xcode should automatically include it in the build
- If missing, verify file is in "IDL RPG Shared" folder and project includes it

**App Size Warnings:**
- Target: Keep app size under 100MB for initial download
- Use asset compression if needed
- Remove unused assets

## Post-Upload

1. **App Store Connect** - Log in and verify build appears
2. **Processing Time** - Wait 10-60 minutes for processing
3. **Select Build** - Choose build version in App Store Connect listing
4. **Complete Metadata** - Ensure all screenshots and metadata are uploaded
5. **Submit for Review** - Follow submission checklist

## Build Configuration Summary

### iOS Target
- Bundle ID: `IDLrpg.IDL-RPG`
- Deployment Target: iOS 15.0
- Team: VZ77AMNZ8N
- Version: 1.0
- Build: 1 (increment for updates)

### macOS Target
- Bundle ID: `IDLrpg.IDL-RPG`
- Deployment Target: macOS 11.0
- Team: VZ77AMNZ8N
- Version: 1.0
- Build: 1 (increment for updates)

---

**Note**: Always test archived builds on physical devices before submission when possible. Use TestFlight for beta testing with external testers.

