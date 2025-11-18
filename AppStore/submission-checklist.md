# App Store Submission Checklist for IDL RPG

Use this checklist to track your App Store submission progress.

## Phase 1: Code Preparation ✅

- [x] Fix deployment target to iOS 15.0
- [x] Fix macOS deployment target to macOS 11.0
- [x] Disable debug overlays (FPS, node count) in release builds
- [x] Verify bundle identifier: `IDLrpg.IDL-RPG`
- [x] Verify code signing team: `VZ77AMNZ8N`
- [x] Create Privacy Manifest (PrivacyInfo.xcprivacy) if needed
- [ ] Test build on physical iOS device
- [ ] Test build on macOS

## Phase 2: App Store Assets

### Visual Assets
- [ ] App Icon (1024x1024px) - iOS
- [ ] App Icon (512x512px to 1024x1024px@2x) - macOS
- [ ] Screenshot - iPhone 6.7" (1290 x 2796)
- [ ] Screenshot - iPhone 6.5" (1242 x 2688)
- [ ] Screenshot - iPhone 5.5" (1242 x 2208)
- [ ] Screenshot - iPad 12.9" (2048 x 2732) - if supporting iPad
- [ ] Screenshot - iPad 11" (1668 x 2388) - if supporting iPad
- [ ] Screenshot - macOS (1280 x 800 or 2560 x 1600)
- [ ] App Preview Video (optional but recommended)

### Metadata
- [ ] App Name: "IDL RPG"
- [ ] Subtitle (30 characters max)
- [ ] Short Description (170 characters)
- [ ] Full Description (up to 4000 characters)
- [ ] Promotional Text (170 characters)
- [ ] Keywords (100 characters, comma-separated)
- [ ] Category: Games > Role Playing
- [ ] Support URL (must be hosted and accessible)
- [ ] Privacy Policy URL (must be hosted and accessible)
- [ ] Support Email
- [ ] Marketing URL (optional)

## Phase 3: App Store Connect Setup

### App Information
- [ ] Create app listing in App Store Connect
- [ ] Set bundle ID: `IDLrpg.IDL-RPG`
- [ ] Upload app icon
- [ ] Upload screenshots for all required sizes
- [ ] Upload app preview video (optional)
- [ ] Fill in all metadata fields
- [ ] Set pricing (Free or Paid)
- [ ] Set availability (countries/regions)

### App Review Information
- [ ] Complete contact information (name, phone, email)
- [ ] Add reviewer notes
- [ ] Set up demo account (if applicable)
- [ ] Complete age rating questionnaire

### Capabilities & Permissions
- [ ] Review and configure app capabilities
- [ ] Add usage descriptions for any required permissions
- [ ] Configure Game Center (if applicable)
- [ ] Configure iCloud (if applicable)

## Phase 4: Build & Archive

### Pre-Build
- [ ] Increment build number
- [ ] Set build configuration to Release
- [ ] Verify all assets are included
- [ ] Run final tests on device

### iOS Archive
- [ ] Select "Any iOS Device" or "Generic iOS Device"
- [ ] Product > Archive
- [ ] Wait for archive completion
- [ ] Validate archive in Organizer
- [ ] Distribute to App Store Connect
- [ ] Resolve any validation errors

### macOS Archive
- [ ] Select "Any Mac"
- [ ] Product > Archive
- [ ] Validate archive
- [ ] Distribute to App Store Connect
- [ ] Resolve any validation errors

## Phase 5: Submission

- [ ] Select build version in App Store Connect
- [ ] Complete all required metadata fields
- [ ] Upload all required screenshots
- [ ] Set release type (Manual/Automatic/Scheduled)
- [ ] Review all submission details
- [ ] Submit for review

## Phase 6: Post-Submission

### Monitoring
- [ ] Set up App Store Connect notifications
- [ ] Check review status daily
- [ ] Be ready to respond to reviewer questions within 24 hours
- [ ] Monitor crash reports (if applicable)

### Common Issues to Watch
- [ ] Missing privacy policy URL
- [ ] Incomplete app functionality
- [ ] App crashes or freezes
- [ ] Guideline violations
- [ ] Missing required metadata

### Post-Approval
- [ ] Monitor crash reports
- [ ] Track user ratings and reviews
- [ ] Prepare update roadmap
- [ ] Set up analytics (if applicable)

## Notes

- Build Number: 1 (increment for each submission)
- Marketing Version: 1.0
- Bundle Identifier: `IDLrpg.IDL-RPG`
- Development Team: VZ77AMNZ8N

---

**Current Status**: Pre-submission preparation  
**Last Updated**: [Date]

