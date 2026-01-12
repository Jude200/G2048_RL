"""Logging configuration"""

import logging
import sys
from pathlib import Path

import yaml

# Load config once
_config = None

def _load_config():
    """Load logging configuration from config.yaml"""
    global _config
    if _config is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                _config = yaml.safe_load(f)
        except FileNotFoundError:
            _config = {}  # Default to empty if no config found
    return _config

def get_logger(name: str, level: int = None) -> logging.Logger:
    """Get a configured logger instance
    
    Args:
        name: Logger name
        level: Optional log level override (uses config if not specified)
    
    Returns:
        Configured logger instance
    """
    config = _load_config()
    log_config = config.get("logging", {})
    
    # Check if logging is enabled
    enabled = log_config.get("enabled", True)
    
    logger = logging.getLogger(name)
    
    if not enabled:
        logger.disabled = True
        return logger
    
    # Determine log level
    if level is None:
        level_str = log_config.get("level", "INFO")
        level = getattr(logging, level_str.upper(), logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    
    return logger
