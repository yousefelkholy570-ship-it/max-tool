#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Max Tool Installer & Setup Script
أداة تثبيت شاملة لـ Max Tool
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# ==================== COLORS ====================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# ==================== INSTALLATION FUNCTIONS ====================

def print_banner():
    """Print welcome banner"""
    banner = f"""
    {Colors.CYAN}{Colors.BOLD}
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║    🚀 Max Tool Advanced v2.0 - Setup Wizard           ║
    ║    Professional Integrated Platform                    ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    {Colors.ENDC}
    """
    print(banner)

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.ENDC}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.ENDC}")

def check_python_version():
    """Check Python version"""
    print_info("Checking Python version...")
    version_info = sys.version_info
    version_string = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 10):
        print_error(f"Python 3.10+ required. Current: {version_string}")
        return False
    
    print_success(f"Python version: {version_string}")
    return True

def check_system_requirements():
    """Check system requirements"""
    print_info("Checking system requirements...")
    
    system = platform.system()
    print_success(f"Operating System: {system} {platform.release()}")
    
    try:
        import psutil
        memory = psutil.virtual_memory()
        print_success(f"Available RAM: {memory.available / (1024**3):.1f} GB")
    except:
        print_warning("Could not check RAM")
    
    return True

def install_dependencies():
    """Install required packages"""
    print_info("Installing Python dependencies...")
    print_info("This may take several minutes...\n")
    
    # Core PyQt6 packages
    core_packages = [
        "PyQt6==6.6.1",
        "PyQt6-Charts==6.6.1",
        "PyQt6-WebEngine==6.6.1",
        "PyQt6-Svg==6.6.1",
    ]
    
    # Essential packages
    essential_packages = [
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "psutil>=5.9.5",
        "requests>=2.31.0",
        "packaging>=23.0",
        "cryptography>=41.0.0",
        "pytest>=7.4.0",
    ]
    
    all_packages = core_packages + essential_packages
    
    print_info(f"Installing {len(all_packages)} packages...\n")
    
    for idx, package in enumerate(all_packages, 1):
        print(f"[{idx}/{len(all_packages)}] Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", package])
            print_success(f"Installed: {package}")
        except subprocess.CalledProcessError:
            print_warning(f"Could not install {package}. Continuing...")
        except Exception as e:
            print_warning(f"Error installing {package}: {e}")
    
    print()
    print_success("Dependencies installation completed!")

def create_directories():
    """Create required directories"""
    print_info("Creating project directories...")
    
    directories = [
        "data",
        "logs",
        "plugins",
        "reports",
        "cache",
        "backups",
        "tests",
        "docs",
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print_success(f"Created directory: {directory}/")
    
    print()

def create_config_file():
    """Create default configuration file"""
    print_info("Creating configuration file...")
    
    config_content = """# Max Tool - Configuration File
# ملف إعدادات Max Tool

[app]
name = Max Tool
version = 2.0.0
author = Professional Team
debug = False

[logging]
level = INFO
max_file_size = 52428800
backup_count = 10
console_output = True

[database]
engine = sqlite
path = data/max_tool.db
echo = False

[gui]
theme = fusion
style = dark
window_width = 1600
window_height = 1000
font_size = 10

[plugins]
directory = plugins
auto_load = True
check_permissions = True
max_plugins = 100

[monitoring]
enabled = True
interval = 5
buffer_size = 1000

[updates]
check_enabled = True
check_interval = 86400
auto_download = False
auto_install = False

[security]
enable_ssl = True
verify_certificates = True
max_retries = 3
timeout = 30

[performance]
async_workers = 4
max_concurrent_tasks = 10
cache_enabled = True
memory_limit = 1073741824
"""
    
    config_path = Path("config.ini")
    if not config_path.exists():
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print_success("Configuration file created: config.ini")
    else:
        print_info("Configuration file already exists")
    
    print()

def create_env_file():
    """Create .env file template"""
    print_info("Creating environment file...")
    
    env_content = """# Max Tool Environment Variables
# متغيرات البيئة

MAX_TOOL_DEBUG=False
MAX_TOOL_LOG_LEVEL=INFO
MAX_TOOL_ENVIRONMENT=production

DATABASE_URL=sqlite:///data/max_tool.db

MONITORING_ENABLED=True
MONITORING_INTERVAL=5

UPDATE_CHECK_ENABLED=True
UPDATE_AUTO_INSTALL=False

SECURITY_ENABLE_SSL=True
SECURITY_VERIFY_CERTIFICATES=True

PERFORMANCE_ASYNC_WORKERS=4
PERFORMANCE_CACHE_SIZE=104857600
"""
    
    env_path = Path(".env")
    if not env_path.exists():
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print_success("Environment file created: .env")
    else:
        print_info("Environment file already exists")
    
    print()

def verify_installation():
    """Verify all installations"""
    print_info("Verifying installation...\n")
    
    packages_to_check = [
        ("PyQt6", "PyQt6"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("psutil", "psutil"),
        ("requests", "requests"),
        ("cryptography", "cryptography"),
    ]
    
    all_ok = True
    
    for package_name, import_name in packages_to_check:
        try:
            __import__(import_name)
            print_success(f"Package installed: {package_name}")
        except ImportError:
            print_error(f"Package missing: {package_name}")
            all_ok = False
    
    print()
    return all_ok

def create_launcher():
    """Create platform-specific launcher scripts"""
    print_info("Creating launcher scripts...")
    
    system = platform.system()
    
    if system == "Windows":
        launcher_content = """@echo off
REM Max Tool Launcher for Windows
echo Starting Max Tool Advanced v2.0...
python max_tool_advanced.py
pause
"""
        launcher_path = Path("launch.bat")
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        print_success("Created launcher: launch.bat")
    
    else:  # Linux/Mac
        launcher_content = """#!/bin/bash
# Max Tool Launcher for Linux/Mac
echo "Starting Max Tool Advanced v2.0..."
python3 max_tool_advanced.py
"""
        launcher_path = Path("launch.sh")
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        os.chmod(launcher_path, 0o755)
        print_success("Created launcher: launch.sh")
    
    print()

def print_final_instructions():
    """Print final setup instructions"""
    print(f"""
    {Colors.GREEN}{Colors.BOLD}
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║    ✓ Installation Completed Successfully!              ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    {Colors.ENDC}
    
    {Colors.CYAN}📋 Next Steps:{Colors.ENDC}
    
    {Colors.BOLD}1. Start the Application:{Colors.ENDC}
       {Colors.YELLOW}Windows:{Colors.ENDC}
       - Run: launch.bat
       - Or: python max_tool_advanced.py
       
       {Colors.YELLOW}Linux/Mac:{Colors.ENDC}
       - Run: ./launch.sh
       - Or: python3 max_tool_advanced.py
    
    {Colors.BOLD}2. Configuration:{Colors.ENDC}
       - Edit config.ini to customize settings
       - Edit .env for environment variables
    
    {Colors.BOLD}3. Create Plugins:{Colors.ENDC}
       - Place plugin files in the plugins/ directory
       - Each plugin needs manifest.json
    
    {Colors.BOLD}4. View Documentation:{Colors.ENDC}
       - Check README.md for detailed information
       - Visit: https://github.com/yousefelkholy570-ship-it/max-tool
    
    {Colors.CYAN}📁 Project Structure:{Colors.ENDC}
    - max_tool_main.py        → Core application
    - max_tool_advanced.py    → Advanced features
    - max_tool_config.py      → Configuration system
    - data/                   → Application data
    - logs/                   → Application logs
    - plugins/                → Custom plugins
    - reports/                → Generated reports
    
    {Colors.CYAN}🔧 Troubleshooting:{Colors.ENDC}
    - If PyQt6 fails to install, try: pip install --upgrade pip
    - For missing dependencies: pip install -r requirements_complete.txt
    - Check logs/ folder for error details
    
    {Colors.CYAN}💡 Useful Commands:{Colors.ENDC}
    - python max_tool_advanced.py    → Run with advanced features
    - python max_tool_main.py        → Run standard version
    - python -m pytest               → Run tests
    - python max_tool_config.py --validate → Validate configuration
    
    {Colors.GREEN}Happy using Max Tool! 🎉{Colors.ENDC}
    """)

# ==================== MAIN ENTRY POINT ====================

def main():
    """Main installation flow"""
    try:
        print_banner()
        
        # Step 1: Check Python version
        if not check_python_version():
            print_error("Setup aborted")
            sys.exit(1)
        
        print()
        
        # Step 2: Check system requirements
        if not check_system_requirements():
            print_warning("Some system checks failed, but continuing...")
        
        print()
        
        # Step 3: Install dependencies
        try:
            install_dependencies()
        except Exception as e:
            print_error(f"Installation failed: {e}")
            print_info("Trying to install core packages...")
        
        # Step 4: Create directories
        create_directories()
        
        # Step 5: Create configuration files
        create_config_file()
        create_env_file()
        
        # Step 6: Verify installation
        if verify_installation():
            print_success("All packages verified!")
        else:
            print_warning("Some packages are missing. Please run: pip install -r requirements_complete.txt")
        
        # Step 7: Create launcher scripts
        create_launcher()
        
        # Step 8: Print final instructions
        print_final_instructions()
        
    except KeyboardInterrupt:
        print_error("\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
