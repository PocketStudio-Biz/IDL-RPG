# IDL RPG - App Store Submission Documentation

## Overview

This directory contains comprehensive documentation for submitting **IDL RPG** to the App Store. All 8 steps of the submission plan have been completed and documented.

---

## Documentation Files

### 1. **APP_STORE_SUBMISSION_PLAN.md**
   Complete 8-step submission plan covering:
   - Requirements definition
   - Design guidelines
   - Development phases
   - Testing plan
   - App Store listing preparation
   - Build & archive process
   - Submission steps
   - Post-submission monitoring

### 2. **APP_STORE_METADATA.md**
   Ready-to-use metadata for App Store Connect:
   - App name and subtitle
   - Full description
   - Keywords
   - URLs (support, privacy, marketing)
   - Category and age rating
   - Review notes template

### 3. **PRIVACY_POLICY.md**
   Complete privacy policy template:
   - No data collection declaration
   - Local storage explanation
   - Compliance with GDPR, CCPA, COPPA
   - Ready to host online

### 4. **BUILD_AND_SUBMIT_GUIDE.md**
   Step-by-step build and submission instructions:
   - Pre-build preparation
   - Archive creation
   - Validation process
   - Upload to App Store Connect
   - Submission checklist

### 5. **SUBMISSION_CHECKLIST.md**
   Quick reference checklist:
   - Pre-development items
   - Development phase checks
   - Pre-submission verification
   - App Store listing completion
   - Submission final steps

### 6. **PrivacyInfo.xcprivacy**
   Privacy manifest file for iOS 17+:
   - Declares no tracking
   - Declares no data collection
   - Required for App Store submission

---

## Quick Start

### For First-Time Submission

1. **Review** `APP_STORE_SUBMISSION_PLAN.md` for complete overview
2. **Prepare** metadata using `APP_STORE_METADATA.md`
3. **Host** privacy policy from `PRIVACY_POLICY.md` online
4. **Follow** `BUILD_AND_SUBMIT_GUIDE.md` step-by-step
5. **Check** `SUBMISSION_CHECKLIST.md` before submitting

### For Updates/Resubmissions

1. **Update** version and build numbers
2. **Review** `BUILD_AND_SUBMIT_GUIDE.md` for build process
3. **Update** "What's New" in App Store Connect
4. **Check** `SUBMISSION_CHECKLIST.md`
5. **Submit** updated build

---

## Important Notes

### ⚠️ Action Required

1. **iOS Deployment Target**: Currently set to `26.1` in project settings. This appears incorrect (iOS 26 doesn't exist). Should be `14.0` or `15.0` per the plan. Update in Xcode:
   - Project → Target → General → Minimum Deployments → iOS 14.0

2. **Privacy Policy URL**: Replace placeholder URLs in metadata files with your actual URLs before submission.

3. **Support Email**: Replace `[your-email@example.com]` with your actual support email.

4. **Debug Code**: Remove debug features before release:
   - `skView.showsFPS = true` in GameViewController.swift
   - `skView.showsNodeCount = true` in GameViewController.swift

5. **Privacy Manifest**: The `PrivacyInfo.xcprivacy` file needs to be added to your Xcode project:
   - File → Add Files to "IDL RPG"
   - Select `PrivacyInfo.xcprivacy`
   - Ensure it's added to "IDL RPG iOS" target

---

## Key Information

### App Details
- **Name**: IDL RPG
- **Bundle ID**: IDLrpg.IDL-RPG
- **Current Version**: 1.0
- **Build**: 1
- **Category**: Games → Role Playing
- **Price**: Free
- **Age Rating**: 4+

### Team Information
- **Development Team**: VZ77AMNZ8N
- **Code Signing**: Automatic

### Platform Support
- **iOS**: iPhone and iPad (Universal)
- **macOS**: Supported (Catalyst)

---

## Submission Workflow

```
1. Development Complete
   ↓
2. Update Version/Build Numbers
   ↓
3. Remove Debug Code
   ↓
4. Create Archive
   ↓
5. Validate Archive
   ↓
6. Upload to App Store Connect
   ↓
7. Complete App Store Listing
   ↓
8. Submit for Review
   ↓
9. Monitor Review Status
   ↓
10. Respond to Feedback (if needed)
```

---

## Next Steps

### Immediate Actions

1. ✅ Review all documentation files
2. ⚠️ Fix iOS deployment target (26.1 → 14.0)
3. ⚠️ Add PrivacyInfo.xcprivacy to Xcode project
4. ⚠️ Remove debug code (FPS counter, node count)
5. ⚠️ Host privacy policy online
6. ⚠️ Update placeholder URLs in metadata

### Before First Submission

1. Complete app development
2. Test thoroughly on multiple devices
3. Create screenshots for all required sizes
4. Prepare all metadata
5. Follow build and submission guide

---

## Resources

### Apple Documentation
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [App Store Connect Help](https://help.apple.com/app-store-connect/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

### Tools
- **Xcode**: Primary development and submission tool
- **App Store Connect**: Submission and management portal
- **Transporter**: Alternative upload tool

### Support
- **Apple Developer Support**: [developer.apple.com/contact](https://developer.apple.com/contact)
- **App Review Board**: Via App Store Connect Resolution Center

---

## File Structure

```
IDL RPG/
├── APP_STORE_SUBMISSION_PLAN.md      # Complete 8-step plan
├── APP_STORE_METADATA.md              # Ready-to-use metadata
├── PRIVACY_POLICY.md                  # Privacy policy template
├── BUILD_AND_SUBMIT_GUIDE.md          # Build instructions
├── SUBMISSION_CHECKLIST.md            # Quick checklist
├── PrivacyInfo.xcprivacy              # Privacy manifest
└── README_SUBMISSION.md               # This file
```

---

## Status

✅ **All 8 Steps Completed**

- [x] Step 1: Define Requirements
- [x] Step 2: Establish Design Guidelines
- [x] Step 3: Code Development Phases
- [x] Step 4: Testing Plan
- [x] Step 5: Prepare App Store Listing
- [x] Step 6: Build & Archive Release
- [x] Step 7: Submit to Store
- [x] Step 8: Post-Submission

**Ready for**: App development completion and first submission

---

**Last Updated**: [Date]
**Documentation Version**: 1.0

