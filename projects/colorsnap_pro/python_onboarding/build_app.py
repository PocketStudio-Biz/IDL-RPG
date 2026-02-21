"""
ColorSnap Pro - Build & Deployment Tool
Builds standalone executables for distribution
"""

import sys
import os
import shutil
import subprocess
import platform
from pathlib import Path
from typing import Optional, List
import argparse


class AppBuilder:
    """Builds ColorSnap Pro for distribution"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.build_dir = self.project_dir / "build"
        self.dist_dir = self.project_dir / "dist"
        self.version = "1.0.0"
        
        # App metadata
        self.app_name = "ColorSnapPro"
        self.bundle_id = "com.mykey.colorsnappro"
        self.description = "Professional color picker tool"
        self.author = "MyKey"
    
    def clean(self):
        """Clean build directories"""
        print("🧹 Cleaning build directories...")
        
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   Removed {dir_path}")
        
        print("✅ Clean complete")
    
    def build_pyinstaller(self, onefile: bool = False, windowed: bool = True):
        """
        Build using PyInstaller
        
        Args:
            onefile: Create single executable file
            windowed: Windowed app (no console)
        """
        print("🔨 Building with PyInstaller...")
        
        # Check if PyInstaller is installed
        try:
            import PyInstaller
        except ImportError:
            print("❌ PyInstaller not installed. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        
        # Build command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name", self.app_name,
            "--clean",
            "--noconfirm",
        ]
        
        if onefile:
            cmd.append("--onefile")
        else:
            cmd.append("--onedir")
        
        if windowed:
            cmd.append("--windowed")
        
        # Icon (if exists)
        icon_path = self.project_dir / "assets" / "icon.ico"
        if icon_path.exists():
            cmd.extend(["--icon", str(icon_path)])
        
        # Add data files
        cmd.extend(["--add-data", f"README.md{os.pathsep}."])
        
        # Version info (Windows)
        if platform.system() == "Windows":
            version_file = self._create_version_file()
            cmd.extend(["--version-file", str(version_file)])
        
        # macOS specific
        if platform.system() == "Darwin":
            cmd.extend([
                "--osx-bundle-identifier", self.bundle_id,
            ])
            
            # Create Info.plist for macOS
            plist_path = self._create_info_plist()
            cmd.extend(["--osx-entitlements-file", str(plist_path)])
        
        # Main script
        cmd.append(str(self.project_dir / "main_app_example.py"))
        
        # Run build
        print(f"   Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Build failed:\n{result.stderr}")
            return False
        
        print("✅ Build complete")
        print(f"   Output: {self.dist_dir / self.app_name}")
        
        return True
    
    def _create_version_file(self) -> Path:
        """Create version file for Windows"""
        version_file = self.build_dir / "version.txt"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        
        content = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({self.version.replace('.', ', ')}, 0),
    prodvers=({self.version.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{self.author}'),
        StringStruct(u'FileDescription', u'{self.description}'),
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'{self.app_name}'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2024 {self.author}'),
        StringStruct(u'OriginalFilename', u'{self.app_name}.exe'),
        StringStruct(u'ProductName', u'{self.app_name}'),
        StringStruct(u'ProductVersion', u'{self.version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
        
        version_file.write_text(content)
        return version_file
    
    def _create_info_plist(self) -> Path:
        """Create Info.plist for macOS"""
        plist_file = self.build_dir / "Info.plist"
        plist_file.parent.mkdir(parents=True, exist_ok=True)
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleDisplayName</key>
    <string>{self.app_name}</string>
    <key>CFBundleExecutable</key>
    <string>{self.app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>{self.bundle_id}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{self.app_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>{self.version}</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.graphics-design</string>
</dict>
</plist>"""
        
        plist_file.write_text(plist_content)
        return plist_file
    
    def create_dmg(self):
        """Create DMG for macOS distribution"""
        if platform.system() != "Darwin":
            print("❌ DMG creation only available on macOS")
            return False
        
        print("📦 Creating DMG...")
        
        app_path = self.dist_dir / f"{self.app_name}.app"
        if not app_path.exists():
            print(f"❌ App not found at {app_path}")
            return False
        
        dmg_name = f"{self.app_name}-{self.version}.dmg"
        dmg_path = self.dist_dir / dmg_name
        
        # Create DMG using create-dmg if available
        try:
            subprocess.run(["create-dmg", "--version"], capture_output=True, check=True)
            
            cmd = [
                "create-dmg",
                "--volname", self.app_name,
                "--window-pos", "200", "120",
                "--window-size", "600", "400",
                "--icon-size", "100",
                "--app-drop-link", "450", "185",
                str(dmg_path),
                str(app_path)
            ]
            
            subprocess.run(cmd, check=True)
            print(f"✅ DMG created: {dmg_path}")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to hdiutil
            print("   Using hdiutil fallback...")
            
            temp_dir = self.build_dir / "dmg_staging"
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            temp_dir.mkdir(parents=True)
            
            # Copy app to staging
            shutil.copytree(app_path, temp_dir / app_path.name)
            
            # Create DMG
            cmd = [
                "hdiutil", "create",
                "-srcfolder", str(temp_dir),
                "-volname", self.app_name,
                "-fs", "HFS+",
                "-format", "UDZO",
                "-o", str(dmg_path)
            ]
            
            subprocess.run(cmd, check=True)
            print(f"✅ DMG created: {dmg_path}")
            return True
    
    def create_installer_windows(self):
        """Create Windows installer using Inno Setup (if available)"""
        if platform.system() != "Windows":
            print("❌ Windows installer creation only available on Windows")
            return False
        
        print("📦 Creating Windows installer...")
        
        # Check for Inno Setup
        iscc_path = Path("C:/Program Files (x86)/Inno Setup 6/ISCC.exe")
        if not iscc_path.exists():
            print("❌ Inno Setup not found. Please install from jrsoftware.org")
            return False
        
        # Create installer script
        iss_script = self.build_dir / "installer.iss"
        iss_content = f"""; Inno Setup Script for ColorSnap Pro
[Setup]
AppName={self.app_name}
AppVersion={self.version}
AppPublisher={self.author}
DefaultDirName={{autopf}}\\{self.app_name}
DefaultGroupName={self.app_name}
OutputDir={self.dist_dir}
OutputBaseFilename={self.app_name}-{self.version}-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "{self.dist_dir / self.app_name}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{{group}}\\{self.app_name}"; Filename: "{{app}}\\{self.app_name}.exe"
Name: "{{autodesktop}}\\{self.app_name}"; Filename: "{{app}}\\{self.app_name}.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{{app}}\\{self.app_name}.exe"; Description: "Launch {self.app_name}"; Flags: nowait postinstall skipifsilent
"""
        
        iss_script.write_text(iss_content)
        
        # Run Inno Setup
        result = subprocess.run([str(iscc_path), str(iss_script)], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Installer created: {self.dist_dir / f'{self.app_name}-{self.version}-Setup.exe'}")
            return True
        else:
            print(f"❌ Installer creation failed:\n{result.stderr}")
            return False
    
    def create_linux_appimage(self):
        """Create Linux AppImage (requires appimagetool)"""
        if platform.system() != "Linux":
            print("❌ AppImage creation only available on Linux")
            return False
        
        print("📦 Creating Linux AppImage...")
        print("   Note: This requires appimagetool to be installed")
        
        # Check for appimagetool
        result = subprocess.run(["which", "appimagetool"], capture_output=True)
        if result.returncode != 0:
            print("❌ appimagetool not found. Install from https://appimage.org/")
            return False
        
        appdir = self.build_dir / f"{self.app_name}.AppDir"
        if appdir.exists():
            shutil.rmtree(appdir)
        
        appdir.mkdir(parents=True)
        
        # Create AppDir structure
        (appdir / "usr" / "bin").mkdir(parents=True)
        (appdir / "usr" / "share" / "applications").mkdir(parents=True)
        (appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True)
        
        # Copy executable
        shutil.copy(
            self.dist_dir / self.app_name / self.app_name,
            appdir / "usr" / "bin" / self.app_name
        )
        
        # Create desktop entry
        desktop_entry = f"""[Desktop Entry]
Name={self.app_name}
Exec={self.app_name}
Icon={self.app_name.lower()}
Type=Application
Categories=Graphics;Design;
Comment={self.description}
"""
        
        (appdir / f"{self.app_name.lower()}.desktop").write_text(desktop_entry)
        (appdir / "usr" / "share" / "applications" / f"{self.app_name.lower()}.desktop").write_text(desktop_entry)
        
        # Create AppRun
        apprun = f"""#!/bin/bash
HERE="$(dirname "$(readlink -f "${{0}}")")"
export PATH="${{HERE}}/usr/bin:${{PATH}}"
exec "${{HERE}}/usr/bin/{self.app_name}" "$@"
"""
        
        (appdir / "AppRun").write_text(apprun)
        os.chmod(appdir / "AppRun", 0o755)
        
        # Build AppImage
        output_file = self.dist_dir / f"{self.app_name}-{self.version}-x86_64.AppImage"
        result = subprocess.run(
            ["appimagetool", str(appdir), str(output_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ AppImage created: {output_file}")
            return True
        else:
            print(f"❌ AppImage creation failed:\n{result.stderr}")
            return False
    
    def run_all(self):
        """Run complete build process"""
        print(f"🚀 Building {self.app_name} v{self.version}")
        print(f"   Platform: {platform.system()}")
        print()
        
        self.clean()
        
        if not self.build_pyinstaller():
            return False
        
        # Platform-specific packaging
        if platform.system() == "Darwin":
            self.create_dmg()
        elif platform.system() == "Windows":
            self.create_installer_windows()
        elif platform.system() == "Linux":
            self.create_linux_appimage()
        
        print()
        print("✨ Build complete!")
        print(f"   Output directory: {self.dist_dir}")
        
        # List output files
        if self.dist_dir.exists():
            print("\n📦 Generated files:")
            for f in sorted(self.dist_dir.iterdir()):
                size = f.stat().st_size / (1024 * 1024)  # MB
                print(f"   {f.name} ({size:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Build ColorSnap Pro")
    parser.add_argument("--clean", action="store_true", help="Clean build directories")
    parser.add_argument("--onefile", action="store_true", help="Create single executable file")
    parser.add_argument("--console", action="store_true", help="Keep console window (for debugging)")
    parser.add_argument("--dmg", action="store_true", help="Create DMG (macOS only)")
    parser.add_argument("--installer", action="store_true", help="Create installer (Windows only)")
    parser.add_argument("--appimage", action="store_true", help="Create AppImage (Linux only)")
    parser.add_argument("--all", action="store_true", help="Run complete build process")
    
    args = parser.parse_args()
    
    builder = AppBuilder()
    
    if args.clean:
        builder.clean()
        return
    
    if args.all:
        builder.run_all()
        return
    
    # Individual builds
    if args.dmg:
        builder.build_pyinstaller()
        builder.create_dmg()
    elif args.installer:
        builder.build_pyinstaller()
        builder.create_installer_windows()
    elif args.appimage:
        builder.build_pyinstaller()
        builder.create_linux_appimage()
    else:
        # Default: just build executable
        builder.build_pyinstaller(
            onefile=args.onefile,
            windowed=not args.console
        )


if __name__ == "__main__":
    main()
