"""
Centralized logging configuration using loguru.
Provides sentry_logger as required by team rules.
"""
import sys
from loguru import logger

# Configure loguru with appropriate formatting and levels
logger.remove()  # Remove default handler

# Add console handler with colored output for development
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# Add file handler for persistent logging
logger.add(
    "logs/app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="30 days",
    compression="zip"
)

# Export as sentry_logger for team rule compliance
sentry_logger = logger 