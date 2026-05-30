#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Dependency Checker
فحص سريع للمكتبات المطلوبة
"""

import sys
import subprocess

required_packages = [
    "PyQt6",
    "PyQt6.QtCharts",
    "PyQt6.QtSvg",
    "numpy",
    "pandas",
    "psutil",
    "requests",
    "cryptography",
]

def check_import(package_name, import_path=None):
    """Check if package can be imported"""
    if import_path is None:
        import_path = package_name
    
    try:
        __import__(import_path)
        print(f"✓ {package_name}")
        return True
    except ImportError:
        print(f"✗ {package_name} - NOT INSTALLED")
        return False

def install_package(package_name):
    """Install missing package"""
    print(f"Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
        return True
    except:
        return False

if __name__ == "__main__":
    print("="*50)
    print("Max Tool - Dependency Checker")
    print("="*50)
    print()
    
    print("Checking installed packages...\n")
    
    missing = []
    for pkg in required_packages:
        if not check_import(pkg):
            missing.append(pkg)
    
    print()
    
    if missing:
        print(f"\n{len(missing)} packages are missing!")
        print(f"\nMissing packages: {', '.join(missing)}")
        print("\nWould you like to install them? (y/n)")
        
        response = input("> ").strip().lower()
        if response == 'y':
            for pkg in missing:
                if not install_package(pkg):
                    print(f"Failed to install {pkg}")
            print("\nDone! Try running the app again.")
        else:
            print("Skipped installation.")
            print("\nRun this to install manually:")
            print(f"pip install -r requirements_complete.txt")
    else:
        print("\n✓ All packages are installed!")
        print("\nYou can now run:")
        print("  python max_tool_advanced.py")
    
    print()
