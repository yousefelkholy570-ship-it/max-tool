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
    window_state: str = "normal"
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
    check_interval: int = 86400
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
    cache_size: int = 104857600
    memory_limit: int = 1073741824
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
    
    logging: LogConfig = field(default_factory=LogConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    gui: GUIConfig = field(default_factory=GUIConfig)
    plugins: PluginConfig = field(default_factory=PluginConfig)
    updates: UpdateConfig = field(default_factory=UpdateConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    
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
            
            if 'app' in parser:
                for key, value in parser['app'].items():
                    if hasattr(self.config, key):
                        setattr(self.config, key, self._parse_value(value))
            
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
        
        parser['app'] = {
            'name': self.config.name,
            'version': self.config.version,
            'author': self.config.author,
            'debug': str(self.config.debug),
        }
        
        parser['logging'] = {k: str(v) for k, v in asdict(self.config.logging).items()}
        parser['database'] = {k: str(v) for k, v in asdict(self.config.database).items()}
        parser['gui'] = {k: str(v) for k, v in asdict(self.config.gui).items()}
        parser['plugins'] = {k: str(v) for k, v in asdict(self.config.plugins).items()}
        parser['updates'] = {k: str(v) for k, v in asdict(self.config.updates).items()}
        parser['security'] = {k: str(v) for k, v in asdict(self.config.security).items()}
        parser['performance'] = {k: str(v) for k, v in asdict(self.config.performance).items()}
        
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
        
        from datetime import datetime
        log_file = log_dir / f"max_tool_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
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

# ==================== ENVIRONMENT MANAGER ====================

class EnvironmentManager:
    """Manage environment variables"""
    
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

if __name__ == "__main__":
    config_mgr = ConfigurationManager()
    config = config_mgr.get_config()
    print(f"App: {config.name} v{config.version}")
    print(f"Environment: {config.environment.value}")
