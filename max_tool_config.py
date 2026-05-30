#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Max Tool - Configuration Module
Professional setup, configuration management, and initialization utilities
"""

import os
import sys
import json
import configparser
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging

# ==================== CONFIGURATION CLASSES ====================

class Environment(Enum):
    """Application environment"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

@dataclass
class LogConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s:%(lineno)d - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    max_file_size: int = 52428800  # 50MB
    backup_count: int = 10
    file_path: str = "logs"
    console_output: bool = True

@dataclass
class DatabaseConfig:
    """Database configuration"""
    engine: str = "sqlite"
    path: str = "data/max_tool.db"
    url: str = "sqlite:///data/max_tool.db"
    echo: bool = False
    pool_size: int = 5
    pool_recycle: int = 3600
    pool_pre_ping: bool = True

@dataclass
class GUIConfig:
    """GUI configuration"""
    theme: str = "fusion"
    style: str = "dark"
    window_width: int = 1400
    window_height: int = 900
    window_state: str = "normal"  # normal, maximized, minimized
    font_family: str = "Segoe UI"
    font_size: int = 10
    accent_color: str = "#2A82DA"
    enable_animations: bool = True
    show_tips_on_startup: bool = True

@dataclass
class PluginConfig:
    """Plugin system configuration"""
    directory: str = "plugins"
    auto_load: bool = True
    check_permissions: bool = True
    verify_signatures: bool = False
    max_plugins: int = 100
    plugin_timeout: int = 30
    isolated_execution: bool = True

@dataclass
class UpdateConfig:
    """Update configuration"""
    check_enabled: bool = True
    check_interval: int = 86400  # 24 hours
    auto_download: bool = False
    auto_install: bool = False
    notify_user: bool = True
    backup_before_update: bool = True
    update_server: str = "https://api.github.com/repos/yousefelkholy570-ship-it/max-tool"

@dataclass
class SecurityConfig:
    """Security configuration"""
    enable_ssl: bool = True
    verify_certificates: bool = True
    max_retries: int = 3
    timeout: int = 30
    require_auth: bool = False
    encrypt_sensitive_data: bool = True
    log_security_events: bool = True
    file_integrity_check: bool = True

@dataclass
class PerformanceConfig:
    """Performance configuration"""
    async_workers: int = 4
    max_concurrent_tasks: int = 10
    cache_enabled: bool = True
    cache_size: int = 104857600  # 100MB
    memory_limit: int = 1073741824  # 1GB
    thread_pool_size: int = 8
    enable_profiling: bool = False

@dataclass
class AppConfig:
    """Main application configuration"""
    name: str = "Max Tool"
    version: str = "1.0.0"
    author: str = "Professional Team"
    description: str = "Professional Integrated Platform"
    license: str = "MIT"
    environment: Environment = Environment.PRODUCTION
    debug: bool = False
    
    # Sub-configurations
    logging: LogConfig = field(default_factory=LogConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    gui: GUIConfig = field(default_factory=GUIConfig)
    plugins: PluginConfig = field(default_factory=PluginConfig)
    updates: UpdateConfig = field(default_factory=UpdateConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    # Paths
    root_path: str = ""
    data_dir: str = "data"
    log_dir: str = "logs"
    cache_dir: str = ".cache"
    config_file: str = "config.ini"
    
    def __post_init__(self):
        if not self.root_path:
            self.root_path = str(Path(__file__).parent)
        self.data_dir = os.path.join(self.root_path, self.data_dir)
        self.log_dir = os.path.join(self.root_path, self.log_dir)
        self.cache_dir = os.path.join(self.root_path, self.cache_dir)
        self.plugins.directory = os.path.join(self.root_path, self.plugins.directory)

# ==================== CONFIGURATION MANAGER ====================

class ConfigurationManager:
    """Central configuration management system"""
    
    def __init__(self, config_file: str = "config.ini"):
        self.config_file = Path(config_file)
        self.config = AppConfig()
        self._ensure_directories()
        self._load_config()
    
    def _ensure_directories(self):
        """Create necessary directories"""
        dirs = [self.config.data_dir, self.config.log_dir, self.config.cache_dir, 
                self.config.plugins.directory]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def _load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            parser = configparser.ConfigParser()
            parser.read(self.config_file)
            
            # Load main configuration
            if 'app' in parser:
                for key, value in parser['app'].items():
                    if hasattr(self.config, key):
                        setattr(self.config, key, self._parse_value(value))
            
            # Load sub-configurations
            self._load_section(parser, 'logging', self.config.logging)
            self._load_section(parser, 'database', self.config.database)
            self._load_section(parser, 'gui', self.config.gui)
            self._load_section(parser, 'plugins', self.config.plugins)
            self._load_section(parser, 'updates', self.config.updates)
            self._load_section(parser, 'security', self.config.security)
            self._load_section(parser, 'performance', self.config.performance)
        else:
            self.save_config()
    
    def _load_section(self, parser: configparser.ConfigParser, section: str, config_obj):
        """Load configuration section"""
        if section in parser:
            for key, value in parser[section].items():
                if hasattr(config_obj, key):
                    setattr(config_obj, key, self._parse_value(value))
    
    @staticmethod
    def _parse_value(value: str) -> Any:
        """Parse configuration value"""
        if value.lower() in ('true', 'yes', 'on'):
            return True
        elif value.lower() in ('false', 'no', 'off'):
            return False
        else:
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    return value
    
    def save_config(self):
        """Save configuration to file"""
        parser = configparser.ConfigParser()
        
        # Save main config
        parser['app'] = {
            'name': self.config.name,
            'version': self.config.version,
            'author': self.config.author,
            'debug': str(self.config.debug),
        }
        
        # Save sub-configs
        parser['logging'] = asdict(self.config.logging)
        parser['database'] = asdict(self.config.database)
        parser['gui'] = asdict(self.config.gui)
        parser['plugins'] = asdict(self.config.plugins)
        parser['updates'] = asdict(self.config.updates)
        parser['security'] = asdict(self.config.security)
        parser['performance'] = asdict(self.config.performance)
        
        with open(self.config_file, 'w') as f:
            parser.write(f)
    
    def get_config(self) -> AppConfig:
        """Get current configuration"""
        return self.config
    
    def update_config(self, section: str, key: str, value: Any):
        """Update configuration value"""
        if hasattr(self.config, section):
            section_obj = getattr(self.config, section)
            if hasattr(section_obj, key):
                setattr(section_obj, key, value)
                self.save_config()
                return True
        return False
    
    def export_config(self, format: str = "json") -> str:
        """Export configuration"""
        if format == "json":
            return json.dumps(asdict(self.config), indent=2)
        elif format == "ini":
            parser = configparser.ConfigParser()
            # Build parser sections
            return str(parser)
        return ""

# ==================== SYSTEM INITIALIZATION ====================

class SystemInitializer:
    """System initialization and setup"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.logger = None
    
    def initialize(self) -> bool:
        """Initialize all system components"""
        try:
            self._setup_directories()
            self._setup_logging()
            self._setup_database()
            self._check_dependencies()
            return True
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False
    
    def _setup_directories(self):
        """Setup required directories"""
        dirs = [
            self.config.data_dir,
            self.config.log_dir,
            self.config.cache_dir,
            self.config.plugins.directory,
        ]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging system"""
        log_dir = Path(self.config.log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger("MaxTool")
        logger.setLevel(getattr(logging, self.config.logging.level))
        
        formatter = logging.Formatter(
            self.config.logging.format,
            datefmt=self.config.logging.date_format
        )
        
        # File handler
        log_file = log_dir / f"max_tool_{__import__('datetime').datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        if self.config.logging.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        self.logger = logger
    
    def _setup_database(self):
        """Setup database"""
        if self.config.database.engine == "sqlite":
            db_path = Path(self.config.database.path)
            db_path.parent.mkdir(parents=True, exist_ok=True)
            if self.logger:
                self.logger.info(f"Database configured: {db_path}")
    
    def _check_dependencies(self):
        """Check required dependencies"""
        required = [
            "PyQt6",
            "requests",
            "packaging",
        ]
        
        missing = []
        for package in required:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing and self.logger:
            self.logger.warning(f"Missing dependencies: {', '.join(missing)}")

# ==================== ENVIRONMENT MANAGER ====================

class EnvironmentManager:
    """Manage environment variables and secrets"""
    
    @staticmethod
    def load_env(env_file: str = ".env") -> Dict[str, str]:
        """Load environment variables from .env file"""
        env_vars = {}
        env_path = Path(env_file)
        
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            env_vars[key.strip()] = value.strip()
        
        return env_vars
    
    @staticmethod
    def save_env(env_vars: Dict[str, str], env_file: str = ".env"):
        """Save environment variables to .env file"""
        with open(env_file, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
    
    @staticmethod
    def get_env(key: str, default: str = None) -> Optional[str]:
        """Get environment variable"""
        return os.getenv(key, default)

# ==================== DEFAULT CONFIGURATION TEMPLATE ====================

DEFAULT_CONFIG_TEMPLATE = """
# Max Tool - Configuration File
# Professional Integrated Platform

[app]
name = Max Tool
version = 1.0.0
author = Professional Team
debug = False

[logging]
level = INFO
format = %%(asctime)s - [%%(levelname)s] - %%(name)s - %%(funcName)s:%%(lineno)d - %%(message)s
max_file_size = 52428800
backup_count = 10

[database]
engine = sqlite
path = data/max_tool.db
echo = False
pool_size = 5

[gui]
theme = fusion
style = dark
window_width = 1400
window_height = 900
font_size = 10

[plugins]
directory = plugins
auto_load = True
check_permissions = True
max_plugins = 100

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
"""

# ==================== SETUP UTILITIES ====================

def create_default_config(config_file: str = "config.ini"):
    """Create default configuration file"""
    with open(config_file, 'w') as f:
        f.write(DEFAULT_CONFIG_TEMPLATE)
    print(f"Default configuration created: {config_file}")

def setup_project():
    """Setup project directories and files"""
    directories = [
        "data",
        "logs",
        ".cache",
        "plugins",
        "tests",
        "docs",
    ]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"Created directory: {dir_name}")
    
    # Create default config
    create_default_config()

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Max Tool Configuration Manager")
    parser.add_argument("--setup", action="store_true", help="Setup project directories")
    parser.add_argument("--create-config", action="store_true", help="Create default config")
    parser.add_argument("--validate", action="store_true", help="Validate configuration")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_project()
    elif args.create_config:
        create_default_config()
    elif args.validate:
        config_mgr = ConfigurationManager()
        print("Configuration is valid!")
        print(f"App Name: {config_mgr.config.name}")
        print(f"Version: {config_mgr.config.version}")
        print(f"Environment: {config_mgr.config.environment.value}")
    else:
        parser.print_help()
