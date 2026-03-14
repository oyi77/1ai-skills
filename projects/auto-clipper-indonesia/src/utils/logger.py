"""
Auto Clipper Indonesia - Logging System
Centralized logging for debugging and error tracking
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# Log directory
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log file with timestamp
log_filename = LOG_DIR / f"auto_clipper_{datetime.now().strftime('%Y%m%d')}.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create logger
logger = logging.getLogger(__name__)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name"""
    return logging.getLogger(name)


def log_info(message: str):
    """Log info message"""
    logger.info(message)


def log_warning(message: str):
    """Log warning message"""
    logger.warning(message)


def log_error(message: str, exc_info: bool = False):
    """Log error message"""
    logger.error(message, exc_info=exc_info)


def log_debug(message: str):
    """Log debug message"""
    logger.debug(message)


if __name__ == "__main__":
    # Test logger
    log_info("Logger initialized successfully")
    log_warning("This is a warning test")
    log_error("This is an error test")
    log_debug("This is a debug test")
    print(f"Logs written to: {log_filename}")